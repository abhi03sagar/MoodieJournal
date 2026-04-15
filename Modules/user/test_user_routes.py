import pytest
from flask import Flask
from flask_jwt_extended import JWTManager
from Modules.user.routes import user_bp


@pytest.fixture
def client():
    app = Flask(__name__)
    app.config["JWT_SECRET_KEY"] = "test-secret-key-long-enough-for-sha256"
    JWTManager(app)
    app.register_blueprint(user_bp, url_prefix='/api/users')

    with app.test_client() as test_client:
        yield test_client


def test_register_success(client, monkeypatch):
    def fake_register_user(username, email, password):
        return {
            "ok": True,
            "message": "User registered successfully.",
            "user_id": "abc123"
        }

    monkeypatch.setattr("Modules.user.routes.register_user", fake_register_user)

    response = client.post(
        '/api/users/register',
        json={"username": "abhi", "email": "abhi@example.com", "password": "secret123"}
    )

    assert response.status_code == 201
    body = response.get_json()
    assert body["status"] == "success"
    assert body["user_id"] == "abc123"


def test_register_validation_error(client, monkeypatch):
    def fake_register_user(username, email, password):
        return {"ok": False, "error": "A valid email is required."}

    monkeypatch.setattr("Modules.user.routes.register_user", fake_register_user)

    response = client.post(
        '/api/users/register',
        json={"username": "abhi", "password": "secret123"}
    )

    assert response.status_code == 400
    assert response.get_json()["status"] == "error"


def test_login_invalid_credentials(client, monkeypatch):
    def fake_login_user(username, email, password):
        return {"ok": False, "error": "Invalid credentials."}

    monkeypatch.setattr("Modules.user.routes.login_user", fake_login_user)

    response = client.post(
        '/api/users/login',
        json={"username": "abhi", "password": "wrongpass"}
    )

    assert response.status_code == 401
    assert response.get_json()["status"] == "error"


def test_login_success_with_username(client, monkeypatch):
    def fake_login_user(username, email, password):
        return {
            "ok": True,
            "message": "Login successful.",
            "user": {
                "id": "abc123",
                "username": "abhi",
                "email": "abhi@example.com"
            }
        }

    monkeypatch.setattr("Modules.user.routes.login_user", fake_login_user)

    response = client.post(
        '/api/users/login',
        json={"username": "abhi", "password": "secret123"}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "success"
    assert body["user"]["username"] == "abhi"
    assert "access_token" in body


def test_login_success_with_email(client, monkeypatch):
    def fake_login_user(username, email, password):
        return {
            "ok": True,
            "message": "Login successful.",
            "user": {
                "id": "abc123",
                "username": "abhi",
                "email": "abhi@example.com"
            }
        }

    monkeypatch.setattr("Modules.user.routes.login_user", fake_login_user)

    response = client.post(
        '/api/users/login',
        json={"email": "abhi@example.com", "password": "secret123"}
    )

    assert response.status_code == 200
    body = response.get_json()
    assert body["status"] == "success"
    assert body["user"]["username"] == "abhi"
    assert "access_token" in body


def test_me_requires_auth(client):
    response = client.get('/api/users/me')
    assert response.status_code == 401


def test_me_success(client, monkeypatch):
    def fake_login_user(username, email, password):
        return {
            "ok": True,
            "message": "Login successful.",
            "user": {
                "id": "abc123",
                "username": "abhi",
                "email": "abhi@example.com"
            }
        }

    monkeypatch.setattr("Modules.user.routes.login_user", fake_login_user)

    login_response = client.post(
        '/api/users/login',
        json={"username": "abhi", "password": "secret123"}
    )
    token = login_response.get_json()["access_token"]

    me_response = client.get(
        '/api/users/me',
        headers={"Authorization": f"Bearer {token}"}
    )

    assert me_response.status_code == 200
    body = me_response.get_json()
    assert body["status"] == "success"
    assert body["user"]["id"] == "abc123"
