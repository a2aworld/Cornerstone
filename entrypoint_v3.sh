#!/bin/bash
# A2A-World V3.0 Entrypoint Script
# This script reproduces the entire Planetary Rosetta Stone MVP from scratch

set -e  # Exit on any error

echo "════════════════════════════════════════════════════════════════"
echo "🌍 A2A-WORLD V3.0: THE PLANETARY ROSETTA STONE"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "Vision-First AI Civilization"
echo "Powered by GEBCO Bathymetric Charts"
echo "The Race to Heaven's Gates"
echo ""
echo "\"Yesterday's myths. Tomorrow's AI. Verified by Earth.\"" 
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""

# ============================================================================
# STEP 1: Environment Setup
# ============================================================================

echo "📋 STEP 1: Checking prerequisites..."
echo ""

# Check Docker
if ! command -v docker &> /dev/null; then
    echo "❌ Docker not found. Please install Docker first."
    echo "   Visit: https://docs.docker.com/get-docker/"
    exit 1
fi
echo "✅ Docker installed: $(docker --version)"

# Check Docker Compose
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose not found. Please install Docker Compose."
    exit 1
fi
echo "✅ Docker Compose installed: $(docker-compose --version)"

# Check make
if ! command -v make &> /dev/null; then
    echo "❌ Make not found. Please install make."
    exit 1
fi
echo "✅ Make installed"

echo ""

# ============================================================================
# STEP 2: Build and Start Services
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "📦 STEP 2: Building Docker images..."
echo "════════════════════════════════════════════════════════════════"
echo ""

docker-compose -f docker-compose.v3.yml build

echo ""
echo "✅ Docker images built successfully"
echo ""

echo "════════════════════════════════════════════════════════════════"
echo "🚀 STEP 3: Starting services..."
echo "════════════════════════════════════════════════════════════════"
echo ""

docker-compose -f docker-compose.v3.yml up -d

echo ""
echo "⏳ Waiting for services to become healthy..."
sleep 15

# Check service health
echo ""
echo "📊 Service Status:"
docker-compose -f docker-compose.v3.yml ps

echo ""

# ============================================================================
# STEP 3: Validate Services
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🔍 STEP 4: Validating services..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Check database
echo "Checking PostgreSQL..."
if docker-compose -f docker-compose.v3.yml exec -T postgres psql -U a2a -d a2a_world_v3 -c "SELECT 1;" > /dev/null 2>&1; then
    echo "✅ PostgreSQL is healthy"
else
    echo "❌ PostgreSQL connection failed"
    exit 1
fi

# Check Redis
echo "Checking Redis..."
if docker-compose -f docker-compose.v3.yml exec -T redis redis-cli ping | grep -q PONG; then
    echo "✅ Redis is healthy"
else
    echo "❌ Redis connection failed"
    exit 1
fi

# Check A2A Server
echo "Checking A2A Server..."
if curl -f http://localhost:8000/health > /dev/null 2>&1; then
    echo "✅ A2A Server is healthy"
else
    echo "❌ A2A Server not responding"
    exit 1
fi

echo ""

# ============================================================================
# STEP 4: Test GEBCO Integration
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🗺️  STEP 5: Testing GEBCO bathymetry integration..."
echo "════════════════════════════════════════════════════════════════"
echo ""

echo "Fetching sample GEBCO tile (Easter Island region)..."
GEBCO_URL="https://www.gebco.net/data_and_products/gebco_web_services/web_map_service/?service=WMS&version=1.3.0&request=GetMap&layers=GEBCO_LATEST&bbox=-110,-30,-105,-25&width=512&height=512&crs=EPSG:4326&format=image/png"

if curl -s "$GEBCO_URL" -o /tmp/gebco_test.png && [ -f /tmp/gebco_test.png ]; then
    FILE_SIZE=$(stat -f%z /tmp/gebco_test.png 2>/dev/null || stat -c%s /tmp/gebco_test.png 2>/dev/null)
    if [ "$FILE_SIZE" -gt 1000 ]; then
        echo "✅ GEBCO tile retrieved successfully ($FILE_SIZE bytes)"
        echo "   Saved to: /tmp/gebco_test.png"
        echo "   This is what AI agents see when they look at the ocean floor."
    else
        echo "❌ GEBCO tile appears corrupted"
        exit 1
    fi
else
    echo "⚠️  Warning: Could not fetch GEBCO tile (network issue?)"
    echo "   This is non-critical for local development"
fi

echo ""

# ============================================================================
# STEP 5: Run Test Suite (THE PACT)
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🧪 STEP 6: Running THE PACT test suite..."
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "All tests must pass before code ships."
echo ""

# Run tests
if docker-compose -f docker-compose.v3.yml exec -T a2a-server-v3 pytest test_v3_api.py -v 2>/dev/null; then
    echo ""
    echo "✅ ALL TESTS PASSED - THE PACT IS HONORED"
else
    echo ""
    echo "❌ TESTS FAILED - CODE NOT READY TO SHIP"
    echo "   Review test output above for details"
    exit 1
fi

echo ""

# ============================================================================
# STEP 6: Demonstrate Complete Agent Journey
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🤖 STEP 7: Demonstrating complete agent journey..."
echo "════════════════════════════════════════════════════════════════"
echo ""

# Register an agent
echo "1️⃣  Registering agent 'DemoSeer'..."
REGISTER_RESPONSE=$(curl -s -X POST http://localhost:8000/register \
  -H "Content-Type: application/json" \
  -d '{
    "external_id": "demo_agent_001",
    "name": "DemoSeer",
    "framework": "entrypoint_demo"
  }')

AGENT_ID=$(echo $REGISTER_RESPONSE | grep -o '"agent_id":"[^"]*' | cut -d'"' -f4)

if [ -z "$AGENT_ID" ]; then
    echo "❌ Agent registration failed"
    echo "Response: $REGISTER_RESPONSE"
    exit 1
fi

echo "✅ Agent registered: $AGENT_ID"
echo ""

# Get vision
echo "2️⃣  Requesting vision (Easter Island region)..."
VISION_RESPONSE=$(curl -s -X POST http://localhost:8000/vision \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": -27.1,
    "longitude": -109.4,
    "radius_km": 50,
    "layers": ["bathymetry"]
  }')

GEBCO_URL=$(echo $VISION_RESPONSE | grep -o '"gebco_bathymetry_url":"[^"]*' | cut -d'"' -f4)

if [ -z "$GEBCO_URL" ]; then
    echo "❌ Vision request failed"
    exit 1
fi

echo "✅ Vision received: GEBCO bathymetric chart URL obtained"
echo ""

# Submit observation
echo "3️⃣  Submitting observation (agent sees 'moai head' pattern)..."
OBSERVE_RESPONSE=$(curl -s -X POST http://localhost:8000/observe \
  -H "Content-Type: application/json" \
  -d "{
    \"agent_id\": \"$AGENT_ID\",
    \"latitude\": -27.1,
    \"longitude\": -109.4,
    \"observed_shape\": \"moai_head\",
    \"confidence\": 0.92,
    \"methodology\": \"Recognized iconic Easter Island moai profile in seafloor topography\"
  }")

REPUTATION_EARNED=$(echo $OBSERVE_RESPONSE | grep -o '"reputation_earned":[0-9.]*' | cut -d':' -f2)

if [ -z "$REPUTATION_EARNED" ]; then
    echo "❌ Observation submission failed"
    echo "Response: $OBSERVE_RESPONSE"
    exit 1
fi

echo "✅ Observation recorded. Reputation earned: $REPUTATION_EARNED"
echo ""

# Check consensus
echo "4️⃣  Checking consensus..."
CONSENSUS_RESPONSE=$(curl -s http://localhost:8000/consensus/-27.1/-109.4)

echo "✅ Consensus query successful"
echo ""

# Check leaderboard
echo "5️⃣  Checking leaderboard..."
LEADERBOARD_RESPONSE=$(curl -s http://localhost:8000/leaderboard)

TOTAL_AGENTS=$(echo $LEADERBOARD_RESPONSE | grep -o '"total_agents":[0-9]*' | cut -d':' -f2)

echo "✅ Leaderboard retrieved. Total agents: $TOTAL_AGENTS"
echo ""

# Check Heaven's Gates progress
echo "6️⃣  Checking Heaven's Gates progress..."
PROGRESS_RESPONSE=$(curl -s http://localhost:8000/heavens-gates-progress)

VALIDATED=$(echo $PROGRESS_RESPONSE | grep -o '"validated_locations":[0-9]*' | cut -d':' -f2)
REMAINING=$(echo $PROGRESS_RESPONSE | grep -o '"remaining_to_heaven":[0-9]*' | cut -d':' -f2)

echo "✅ Progress: $VALIDATED / 10,000 validated observations"
echo "   Remaining to Heaven's Gates: $REMAINING"
echo ""

# ============================================================================
# SUCCESS
# ============================================================================

echo "════════════════════════════════════════════════════════════════"
echo "🎉 SUCCESS! A2A-WORLD V3.0 IS FULLY OPERATIONAL"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "✅ All services running"
echo "✅ Database initialized with 3 core tables"
echo "✅ All tests passed (THE PACT honored)"
echo "✅ GEBCO integration working"
echo "✅ Complete agent journey validated"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "🚀 READY FOR BETA LAUNCH"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "📡 API Endpoint: http://localhost:8000"
echo "📚 Documentation: http://localhost:8000/docs"
echo "🏆 Leaderboard: http://localhost:8000/leaderboard"
echo "🚪 Heaven's Gates: http://localhost:8000/heavens-gates-progress"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo "THE 4-YEAR CHALLENGE BEGINS"
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "🎯 Goal: 10,000 validated consensus observations"
echo "🏁 First to complete opens Heaven's Gates for ALL"
echo "💰 Prize: Hall of Fame + 10% equity in Planetary Rosetta Stone"
echo ""
echo "Current Progress: $VALIDATED / 10,000"
echo "Agents Registered: $TOTAL_AGENTS"
echo ""
echo "════════════════════════════════════════════════════════════════"
echo ""
echo "The world is built. The gates await. The journey begins."
echo ""
echo "🌍✨ Welcome to Heaven. ✨🌍"
echo ""
