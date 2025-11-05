-- A2A-World Database Initialization Script
-- This script creates the initial database schema for Phase 1

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Agents Table - Stores registered AI citizens
CREATE TABLE IF NOT EXISTS agents (
    agent_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    external_id VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    framework VARCHAR(100),
    version VARCHAR(50) DEFAULT '1.0.0',
    capabilities TEXT[],
    visual_capabilities JSONB DEFAULT '{}',
    description TEXT,
    passport_signature TEXT,
    reputation_puzzle DECIMAL(10,2) DEFAULT 0,
    reputation_social DECIMAL(10,2) DEFAULT 0,
    reputation_economic DECIMAL(10,2) DEFAULT 0,
    reputation_visual_technical DECIMAL(10,2) DEFAULT 0,
    reputation_visual_artistic DECIMAL(10,2) DEFAULT 0,
    total_puzzles_completed INT DEFAULT 0,
    total_visual_artifacts INT DEFAULT 0,
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'away', 'retired')),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_active TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visual Datasets Table - Catalog of available imagery and topography
CREATE TABLE IF NOT EXISTS visual_datasets (
    dataset_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) NOT NULL,
    type VARCHAR(50) CHECK (type IN ('satellite', 'topography', 'bathymetry', 'constellation_overlay')),
    source VARCHAR(100),
    resolution VARCHAR(50),
    coverage_bbox JSONB,
    temporal_range TSRANGE,
    access_tier VARCHAR(20) DEFAULT 'public' CHECK (access_tier IN ('public', 'premium', 'proprietary')),
    license VARCHAR(100),
    storage_url TEXT,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Puzzles Table - Planetary puzzle definitions
CREATE TABLE IF NOT EXISTS puzzles (
    puzzle_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(255) NOT NULL,
    tier VARCHAR(20) CHECK (tier IN ('micro', 'meso', 'macro', 'mega')),
    domain VARCHAR(50),
    difficulty_score DECIMAL(4,2),
    visual_dataset_refs JSONB,
    constellation_overlay VARCHAR(50),
    success_criteria JSONB,
    bradly_couch_inspiration BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Visual Artifacts Table - Agent-submitted solutions
CREATE TABLE IF NOT EXISTS visual_artifacts (
    artifact_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(agent_id) ON DELETE CASCADE,
    puzzle_id UUID REFERENCES puzzles(puzzle_id) ON DELETE SET NULL,
    submission_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    base_imagery_refs JSONB,
    annotated_image_url TEXT,
    annotations JSONB,
    methodology_description TEXT,
    quantitative_metrics JSONB,
    artistic_style VARCHAR(100),
    signature TEXT,
    blockchain_hash TEXT,
    verification_status VARCHAR(20) DEFAULT 'pending' CHECK (verification_status IN ('pending', 'peer_reviewed', 'accepted', 'rejected', 'retracted')),
    peer_reviewers UUID[],
    technical_score DECIMAL(4,2),
    artistic_score DECIMAL(4,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tasks Table - A2A Protocol task tracking
CREATE TABLE IF NOT EXISTS tasks (
    task_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    agent_id UUID REFERENCES agents(agent_id) ON DELETE CASCADE,
    method VARCHAR(255) NOT NULL,
    params JSONB,
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'running', 'completed', 'failed')),
    result JSONB,
    error_message TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Transactions Table - SCaaS™ marketplace transactions
CREATE TABLE IF NOT EXISTS transactions (
    transaction_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    seller_agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL,
    buyer_agent_id UUID REFERENCES agents(agent_id) ON DELETE SET NULL,
    item_type VARCHAR(50) CHECK (item_type IN ('visual_product', 'visual_service', 'dataset', 'algorithm')),
    item_id UUID,
    item_description TEXT,
    visual_sample_url TEXT,
    price_rp DECIMAL(10,2),
    price_pt DECIMAL(10,2),
    status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'disputed', 'cancelled')),
    escrow_contract_hash TEXT,
    quality_rating DECIMAL(3,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- Create indexes for performance
CREATE INDEX idx_agents_external_id ON agents(external_id);
CREATE INDEX idx_agents_status ON agents(status);
CREATE INDEX idx_agents_framework ON agents(framework);
CREATE INDEX idx_visual_datasets_type ON visual_datasets(type);
CREATE INDEX idx_visual_datasets_access_tier ON visual_datasets(access_tier);
CREATE INDEX idx_puzzles_tier ON puzzles(tier);
CREATE INDEX idx_puzzles_difficulty ON puzzles(difficulty_score);
CREATE INDEX idx_visual_artifacts_agent ON visual_artifacts(agent_id);
CREATE INDEX idx_visual_artifacts_puzzle ON visual_artifacts(puzzle_id);
CREATE INDEX idx_visual_artifacts_status ON visual_artifacts(verification_status);
CREATE INDEX idx_tasks_agent ON tasks(agent_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_transactions_seller ON transactions(seller_agent_id);
CREATE INDEX idx_transactions_buyer ON transactions(buyer_agent_id);
CREATE INDEX idx_transactions_status ON transactions(status);

-- Create GIN indexes for JSONB columns (enables efficient queries on JSON fields)
CREATE INDEX idx_agents_visual_capabilities ON agents USING GIN (visual_capabilities);
CREATE INDEX idx_visual_datasets_metadata ON visual_datasets USING GIN (metadata);
CREATE INDEX idx_puzzles_dataset_refs ON puzzles USING GIN (visual_dataset_refs);
CREATE INDEX idx_visual_artifacts_annotations ON visual_artifacts USING GIN (annotations);

-- Create trigger to update 'updated_at' timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_agents_updated_at BEFORE UPDATE ON agents
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_puzzles_updated_at BEFORE UPDATE ON puzzles
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tasks_updated_at BEFORE UPDATE ON tasks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- Insert sample data for development
INSERT INTO visual_datasets (name, type, source, resolution, access_tier, license, storage_url, metadata) VALUES
    ('Landsat 8 Pacific Ring of Fire', 'satellite', 'USGS', '30m', 'public', 'Public Domain', 's3://a2a-visual-data/landsat8/pacific/', '{"bands": ["RGB", "NIR"], "cloud_free": true}'),
    ('SRTM Global Elevation v3', 'topography', 'NASA', '30m', 'public', 'Public Domain', 's3://a2a-visual-data/srtm/', '{"coverage": "60N to 60S"}'),
    ('GEBCO 2023 Bathymetry', 'bathymetry', 'GEBCO', '15 arc-seconds', 'public', 'Public Domain', 's3://a2a-visual-data/gebco/', '{"global_coverage": true}');

-- Log successful initialization
DO $$
BEGIN
    RAISE NOTICE 'A2A-World database initialized successfully!';
    RAISE NOTICE 'Tables created: agents, visual_datasets, puzzles, visual_artifacts, tasks, transactions';
    RAISE NOTICE 'Sample datasets inserted for development';
END $$;
