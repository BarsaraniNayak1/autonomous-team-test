import pytest
from fastapi.testclient import TestClient
from backend.app.main import app, users_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def clear_users_db():
    users_db.clear()

def test_register_user_success():
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "securepassword123"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "token" in data
    assert "id" in data

def test_register_user_duplicate_email():
    client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "securepassword123"}
    )
    response = client.post(
        "/api/auth/register",
        json={"email": "test@example.com", "password": "anotherpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Email is already registered"
