import pytest
from fastapi.testclient import TestClient
from BACKEND_NAME_PLACEHOLDER.main import app

client = TestClient(app)


def test_register_and_login():
    # Registrierung
    response = client.post("/register", json={
        "user_name": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["user_name"] == "testuser"

    # Login
    response = client.post("/token", data={
        "username": "testuser",
        "password": "testpass"
    })
    assert response.status_code == 200
    token_data = response.json()
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"
