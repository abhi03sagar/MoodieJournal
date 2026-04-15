import pytest
from app import app as flask_app


@pytest.fixture
def client():
    flask_app.config["TESTING"] = True
    flask_app.config["JWT_SECRET_KEY"] = "test-secret-key-long-enough-for-sha256"
    with flask_app.test_client() as test_client:
        yield test_client


@pytest.fixture
def auth_header(client, monkeypatch):
    def fake_login_user(username, email, password):
        return {
            "ok": True,
            "message": "Login successful.",
            "user": {
                "id": "u-001",
                "username": "abhi",
                "email": "abhi@example.com",
            },
        }

    monkeypatch.setattr("Modules.user.routes.login_user", fake_login_user)

    response = client.post(
        "/api/users/login",
        json={"username": "abhi", "password": "secret123"},
    )
    token = response.get_json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_history_requires_auth(client):
    response = client.get("/api/history")
    assert response.status_code == 401


def test_history_returns_token_user_entries(client, auth_header, monkeypatch):
    captured = {"user_id": None}

    def fake_get_entries_for_user(user_id):
        captured["user_id"] = user_id
        return [{"_id": "1", "text": "entry", "sentiment": "POSITIVE", "confidence": 0.9}]

    monkeypatch.setattr("app.get_entries_for_user", fake_get_entries_for_user)

    response = client.get("/api/history", headers=auth_header)
    assert response.status_code == 200
    assert captured["user_id"] == "u-001"
    assert isinstance(response.get_json(), list)


def test_history_ignores_query_user_id(client, auth_header, monkeypatch):
    captured = {"user_id": None}

    def fake_get_entries_for_user(user_id):
        captured["user_id"] = user_id
        return []

    monkeypatch.setattr("app.get_entries_for_user", fake_get_entries_for_user)

    response = client.get("/api/history?user_id=attacker", headers=auth_header)
    assert response.status_code == 200
    assert captured["user_id"] == "u-001"
