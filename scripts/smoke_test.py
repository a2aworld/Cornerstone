from fastapi.testclient import TestClient
from a2aworld.a2a_gateway.main import app


def test_health():
    client = TestClient(app)
    r = client.get("/health")
    assert r.status_code == 200
    j = r.json()
    assert j.get("status") == "ok"
    assert j.get("service") == "A2A-World Gateway"


if __name__ == "__main__":
    # Run the test directly
    test_health()
    print("Smoke test passed: /health endpoint")
