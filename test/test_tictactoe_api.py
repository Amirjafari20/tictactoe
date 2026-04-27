import pytest
from fastapi.testclient import TestClient
from BACKEND_NAME_PLACEHOLDER.api._app import build_app

app = build_app()
client = TestClient(app)

def test_root():
    resp = client.get("/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "TicTacToe API Root"

def test_register_and_login():
    username = "testuser"
    password = "testpass"
    # Register
    resp = client.post("/register", json={"user_name": username, "password": password})
    assert resp.status_code == 200
    # Login
    resp = client.post("/token", data={"username": username, "password": password})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    return data["access_token"]

def test_create_game():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.post("/games", json={"player_x": "testuser"}, headers=headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["player_x"] == "testuser"
    assert data["board"] == "         "
    assert data["current_player"] == "X"
    assert data["status"] == "waiting"

def test_invalid_move():
    token = test_register_and_login()
    headers = {"Authorization": f"Bearer {token}"}
    # Create game
    resp = client.post("/games", json={"player_x": "testuser"}, headers=headers)
    game_id = resp.json()["id"]
    # Invalid move (out of bounds)
    resp = client.put(f"/games/{game_id}/move/10", headers=headers)
    assert resp.status_code == 400
    assert "Invalid move" in resp.json()["detail"]
