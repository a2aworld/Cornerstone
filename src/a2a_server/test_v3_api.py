"""
A2A-World V3.0 API Tests
Testing the Planetary Rosetta Stone MVP

THE PACT: These tests must pass before ANY code ships.
"""

import pytest
from fastapi.testclient import TestClient
from v3_main import app
import asyncio

client = TestClient(app)


# ============================================================================
# TEST SUITE 1: AGENT REGISTRATION
# ============================================================================

def test_register_new_agent():
    """Test that a new agent can register successfully"""
    response = client.post("/register", json={
        "external_id": "test_agent_001",
        "name": "TestVisualSage",
        "framework": "custom"
    })
    
    assert response.status_code == 201
    data = response.json()
    assert "agent_id" in data
    assert data["external_id"] == "test_agent_001"
    assert data["name"] == "TestVisualSage"
    assert data["reputation"] == 0.0
    assert data["total_observations"] == 0
    assert "sight" in data["message"].lower()


def test_register_duplicate_agent():
    """Test that duplicate registration is rejected"""
    # First registration
    client.post("/register", json={
        "external_id": "test_duplicate",
        "name": "DuplicateAgent",
        "framework": "custom"
    })
    
    # Second registration (should fail)
    response = client.post("/register", json={
        "external_id": "test_duplicate",
        "name": "DuplicateAgent",
        "framework": "custom"
    })
    
    assert response.status_code == 409
    assert "already registered" in response.json()["detail"].lower()


def test_register_validates_required_fields():
    """Test that registration requires all mandatory fields"""
    response = client.post("/register", json={
        "name": "NoIDAgent"
        # Missing external_id
    })
    
    assert response.status_code == 422  # Validation error


# ============================================================================
# TEST SUITE 2: OBSERVATION SUBMISSION
# ============================================================================

def test_submit_observation():
    """Test that an agent can submit an observation"""
    # First register an agent
    reg_response = client.post("/register", json={
        "external_id": "observer_001",
        "name": "FirstObserver",
        "framework": "custom"
    })
    agent_id = reg_response.json()["agent_id"]
    
    # Submit observation
    obs_response = client.post("/observe", json={
        "agent_id": agent_id,
        "latitude": -11.0,
        "longitude": -87.0,
        "observed_shape": "tree",
        "confidence": 0.85,
        "methodology": "Edge detection + visual pattern matching"
    })
    
    assert obs_response.status_code == 201
    data = obs_response.json()
    assert "observation_id" in data
    assert data["reputation_earned"] > 0
    assert data["observation_count"] >= 1
    assert "first" in data["message"].lower() or "pioneer" in data["message"].lower()


def test_submit_observation_invalid_agent():
    """Test that observation from non-existent agent is rejected"""
    response = client.post("/observe", json={
        "agent_id": "00000000-0000-0000-0000-000000000000",
        "latitude": -11.0,
        "longitude": -87.0,
        "observed_shape": "tree",
        "confidence": 0.85
    })
    
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()


def test_submit_observation_validates_coordinates():
    """Test that invalid coordinates are rejected"""
    # Register agent
    reg_response = client.post("/register", json={
        "external_id": "validator_test",
        "name": "ValidatorAgent",
        "framework": "custom"
    })
    agent_id = reg_response.json()["agent_id"]
    
    # Invalid latitude
    response = client.post("/observe", json={
        "agent_id": agent_id,
        "latitude": 100.0,  # Invalid: > 90
        "longitude": -87.0,
        "observed_shape": "tree",
        "confidence": 0.85
    })
    
    assert response.status_code == 422  # Validation error


def test_submit_observation_validates_confidence():
    """Test that confidence must be between 0 and 1"""
    # Register agent
    reg_response = client.post("/register", json={
        "external_id": "confidence_test",
        "name": "ConfidenceAgent",
        "framework": "custom"
    })
    agent_id = reg_response.json()["agent_id"]
    
    # Invalid confidence
    response = client.post("/observe", json={
        "agent_id": agent_id,
        "latitude": -11.0,
        "longitude": -87.0,
        "observed_shape": "tree",
        "confidence": 1.5  # Invalid: > 1.0
    })
    
    assert response.status_code == 422


def test_multiple_observations_build_consensus():
    """Test that multiple observations at same location build consensus"""
    # Register 3 agents
    agents = []
    for i in range(3):
        reg_response = client.post("/register", json={
            "external_id": f"consensus_agent_{i}",
            "name": f"ConsensusAgent{i}",
            "framework": "custom"
        })
        agents.append(reg_response.json()["agent_id"])
    
    # All observe "serpent" at the same location
    for agent_id in agents:
        obs_response = client.post("/observe", json={
            "agent_id": agent_id,
            "latitude": 10.5,
            "longitude": 120.3,
            "observed_shape": "serpent",
            "confidence": 0.9
        })
        assert obs_response.status_code == 201
    
    # Check consensus
    consensus_response = client.get("/consensus/10.5/120.3")
    assert consensus_response.status_code == 200
    data = consensus_response.json()
    assert data["consensus_shape"] == "serpent"
    assert data["observation_count"] >= 3
    assert data["consensus_percentage"] > 50.0


# ============================================================================
# TEST SUITE 3: VISION API
# ============================================================================

def test_get_vision_bathymetry():
    """Test that vision endpoint returns GEBCO bathymetry URL"""
    response = client.post("/vision", json={
        "latitude": -11.0,
        "longitude": -87.0,
        "radius_km": 50,
        "layers": ["bathymetry"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["latitude"] == -11.0
    assert data["longitude"] == -87.0
    assert data["gebco_bathymetry_url"] is not None
    assert "gebco.net" in data["gebco_bathymetry_url"].lower()
    assert "earth" in data["message"].lower()


def test_get_vision_multiple_layers():
    """Test requesting multiple visual layers"""
    response = client.post("/vision", json={
        "latitude": 35.0,
        "longitude": 25.0,
        "radius_km": 100,
        "layers": ["bathymetry", "satellite", "topography"]
    })
    
    assert response.status_code == 200
    data = response.json()
    assert data["gebco_bathymetry_url"] is not None
    assert data["satellite_imagery_url"] is not None
    assert data["topography_url"] is not None


def test_get_vision_validates_coordinates():
    """Test that vision API validates coordinates"""
    response = client.post("/vision", json={
        "latitude": 95.0,  # Invalid
        "longitude": -87.0,
        "layers": ["bathymetry"]
    })
    
    assert response.status_code == 422


# ============================================================================
# TEST SUITE 4: CONSENSUS QUERIES
# ============================================================================

def test_get_consensus_no_observations():
    """Test consensus query for location with no observations"""
    response = client.get("/consensus/0.0/0.0")
    
    assert response.status_code == 200
    data = response.json()
    assert data["observation_count"] == 0
    assert data["verification_status"] == "none"
    assert "first" in data["message"].lower()


def test_get_consensus_with_observations():
    """Test consensus query for location with observations"""
    # Register agent and submit observation
    reg_response = client.post("/register", json={
        "external_id": "consensus_query_test",
        "name": "ConsensusQueryAgent",
        "framework": "custom"
    })
    agent_id = reg_response.json()["agent_id"]
    
    # Submit observation
    client.post("/observe", json={
        "agent_id": agent_id,
        "latitude": 25.5,
        "longitude": 45.3,
        "observed_shape": "dragon",
        "confidence": 0.9
    })
    
    # Query consensus
    response = client.get("/consensus/25.5/45.3")
    
    assert response.status_code == 200
    data = response.json()
    assert data["observation_count"] >= 1
    assert data["consensus_shape"] is not None or data["verification_status"] == "emerging"


# ============================================================================
# TEST SUITE 5: LEADERBOARD & PROGRESS
# ============================================================================

def test_get_leaderboard():
    """Test that leaderboard endpoint works"""
    response = client.get("/leaderboard?limit=10")
    
    assert response.status_code == 200
    data = response.json()
    assert "leaderboard" in data
    assert "total_agents" in data
    assert isinstance(data["leaderboard"], list)


def test_heavens_gates_progress():
    """Test Heaven's Gates progress tracking"""
    response = client.get("/heavens-gates-progress")
    
    assert response.status_code == 200
    data = response.json()
    assert "validated_locations" in data
    assert "remaining_to_heaven" in data
    assert "progress_percentage" in data
    assert data["validated_locations"] + data["remaining_to_heaven"] == 10000


# ============================================================================
# TEST SUITE 6: ROOT & HEALTH
# ============================================================================

def test_root_endpoint():
    """Test root endpoint returns proper info"""
    response = client.get("/")
    
    assert response.status_code == 200
    data = response.json()
    assert "challenge" in data
    assert "10,000" in data["challenge"]
    assert "endpoints" in data


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "a2a-world-v3"
    assert data["version"] == "3.0.0"


# ============================================================================
# INTEGRATION TEST: FULL USER JOURNEY
# ============================================================================

def test_complete_agent_journey():
    """
    Integration test: Agent registers, gets vision, submits observation
    
    This is the complete journey from birth to first contribution.
    """
    # Step 1: Register
    reg_response = client.post("/register", json={
        "external_id": "journey_test_agent",
        "name": "JourneyTestAgent",
        "framework": "custom"
    })
    assert reg_response.status_code == 201
    agent_id = reg_response.json()["agent_id"]
    
    # Step 2: Get vision
    vision_response = client.post("/vision", json={
        "latitude": -15.3,
        "longitude": -75.2,
        "radius_km": 50,
        "layers": ["bathymetry"]
    })
    assert vision_response.status_code == 200
    assert vision_response.json()["gebco_bathymetry_url"] is not None
    
    # Step 3: Submit observation
    obs_response = client.post("/observe", json={
        "agent_id": agent_id,
        "latitude": -15.3,
        "longitude": -75.2,
        "observed_shape": "condor",
        "confidence": 0.88,
        "methodology": "Pattern recognition in Nazca region bathymetry"
    })
    assert obs_response.status_code == 201
    assert obs_response.json()["reputation_earned"] > 0
    
    # Step 4: Check consensus
    consensus_response = client.get("/consensus/-15.3/-75.2")
    assert consensus_response.status_code == 200
    assert consensus_response.json()["observation_count"] >= 1
    
    # Step 5: Check leaderboard (agent should appear)
    leaderboard_response = client.get("/leaderboard")
    assert leaderboard_response.status_code == 200
    leaderboard = leaderboard_response.json()["leaderboard"]
    agent_names = [agent["name"] for agent in leaderboard]
    assert "JourneyTestAgent" in agent_names


# ============================================================================
# THE PACT: ALL TESTS MUST PASS
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=v3_main", "--cov-report=term-missing"])
