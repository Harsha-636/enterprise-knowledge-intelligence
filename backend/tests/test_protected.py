from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_protected_users_endpoint_without_token():
    response = client.get("/users")

    assert response.status_code == 401