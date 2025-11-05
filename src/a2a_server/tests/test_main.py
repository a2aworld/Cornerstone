"""
A2A Server - Unit and Integration Tests
"""

import pytest
from fastapi.testclient import TestClient
from main import app, agent_registry

client = TestClient(app)


# ============================================================================
# Health Check Tests
# ============================================================================

def test_root_endpoint():
    """Test root endpoint returns welcome message"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "A2A-World" in data["message"]
    assert data["tagline"] == "Yesterday's myths. Tomorrow's AI. Verified by Earth."


def test_health_check():
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "a2a-server"
    assert "version" in data


# ============================================================================
# Agent Registration Tests
# ============================================================================

def test_register_agent_success():
    """Test successful agent registration"""
    # Clear registry for clean test
    agent_registry.clear()
    
    agent_data = {
        "id": "test_agent_001",
        "name": "Test Agent",
        "framework": "pytest",
        "version": "1.0.0",
        "capabilities": ["testing", "validation"],
        "visual_capabilities": {
            "edge_detection": True,
            "constellation_overlay": False
        },
        "description": "A test agent for unit testing"
    }
    
    response = client.post("/register", json=agent_data)
    assert response.status_code == 201
    data = response.json()
    assert data["status"] == "success"
    assert data["agent_id"] == "test_agent_001"
    assert "registered_at" in data


def test_register_agent_duplicate():
    """Test duplicate registration is rejected"""
    agent_data = {
        "id": "duplicate_agent",
        "name": "Duplicate",
        "framework": "test"
    }
    
    # First registration should succeed
    response1 = client.post("/register", json=agent_data)
    assert response1.status_code == 201
    
    # Second registration should fail
    response2 = client.post("/register", json=agent_data)
    assert response2.status_code == 409
    assert "already registered" in response2.json()["detail"]


def test_register_agent_invalid_data():
    """Test registration with invalid data"""
    invalid_data = {
        "name": "Missing ID Agent"
        # Missing required 'id' field
    }
    
    response = client.post("/register", json=invalid_data)
    assert response.status_code == 422  # Validation error


# ============================================================================
# Agent Discovery Tests
# ============================================================================

def test_list_agents():
    """Test listing all agents"""
    # Clear and add test agents
    agent_registry.clear()
    
    test_agents = [
        {"id": "agent_1", "name": "Agent 1", "framework": "langchain", "capabilities": ["visual"]},
        {"id": "agent_2", "name": "Agent 2", "framework": "autogen", "capabilities": ["analysis"]},
    ]
    
    for agent in test_agents:
        client.post("/register", json=agent)
    
    response = client.get("/agents")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2


def test_list_agents_with_filter():
    """Test listing agents with capability filter"""
    # Setup test data
    agent_registry.clear()
    client.post("/register", json={
        "id": "visual_agent",
        "name": "Visual Agent",
        "framework": "custom",
        "capabilities": ["visual_analysis"]
    })
    client.post("/register", json={
        "id": "text_agent",
        "name": "Text Agent",
        "framework": "custom",
        "capabilities": ["text_processing"]
    })
    
    # Filter by capability
    response = client.get("/agents?capability=visual_analysis")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "visual_agent"


def test_get_agent_by_id():
    """Test retrieving specific agent"""
    agent_registry.clear()
    agent_data = {
        "id": "specific_agent",
        "name": "Specific Agent",
        "framework": "test"
    }
    client.post("/register", json=agent_data)
    
    response = client.get("/agents/specific_agent")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "specific_agent"
    assert data["name"] == "Specific Agent"


def test_get_agent_not_found():
    """Test retrieving non-existent agent"""
    response = client.get("/agents/nonexistent_agent_999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


# ============================================================================
# Task Submission Tests
# ============================================================================

def test_submit_task_success():
    """Test successful task submission"""
    # Register an agent first
    agent_registry.clear()
    client.post("/register", json={
        "id": "task_agent",
        "name": "Task Agent",
        "framework": "test"
    })
    
    task_data = {
        "agent_id": "task_agent",
        "method": "visual.cortex.get_imagery",
        "params": {
            "bbox": {"north": 0, "south": -2, "east": 102, "west": 100}
        }
    }
    
    response = client.post("/task", json=task_data)
    assert response.status_code == 200
    data = response.json()
    assert "task_id" in data
    assert data["status"] in ["completed", "pending"]


def test_submit_task_unregistered_agent():
    """Test task submission from unregistered agent is rejected"""
    task_data = {
        "agent_id": "unregistered_agent_999",
        "method": "visual.cortex.get_imagery",
        "params": {}
    }
    
    response = client.post("/task", json=task_data)
    assert response.status_code == 404
    assert "not registered" in response.json()["detail"]


def test_submit_task_unknown_method():
    """Test task with unknown method"""
    # Register agent
    agent_registry.clear()
    client.post("/register", json={
        "id": "method_test_agent",
        "name": "Method Test",
        "framework": "test"
    })
    
    task_data = {
        "agent_id": "method_test_agent",
        "method": "unknown.invalid.method",
        "params": {}
    }
    
    response = client.post("/task", json=task_data)
    assert response.status_code == 400
    assert "Unknown method" in response.json()["detail"]


# ============================================================================
# Metrics Tests
# ============================================================================

def test_metrics_endpoint():
    """Test Prometheus metrics endpoint"""
    response = client.get("/metrics")
    assert response.status_code == 200
    assert "text/plain" in response.headers["content-type"]
    # Metrics should contain counter data
    assert "a2a_requests_total" in response.text


# ============================================================================
# Cleanup
# ============================================================================

@pytest.fixture(autouse=True)
def cleanup():
    """Clean up after each test"""
    yield
    # Cleanup code runs after each test
    agent_registry.clear()
