from fastapi.testclient import TestClient

from backend.app.main import app


client = TestClient(app)


def test_register():
    response = client.post(
        "/auth/register",
        json={
            "email": "pytest_test@example.com",
            "password": "TestPassword123!",
        },
    )

    assert response.status_code in [200, 400]