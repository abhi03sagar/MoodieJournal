import pytest
from flask import Flask
from Modules.sentiment.routes import sentiment_bp

@pytest.fixture

def client():
    app = Flask(__name__)
    app.register_blueprint(sentiment_bp, url_prefix='/api/sentiment')
    
    with app.test_client() as client:
        yield client

def test_analyse_success(client):
    payload = {"text": "I am feeling great today!"}
    response = client.post('/api/sentiment/analyse', json=payload)
    assert response.status_code == 200
    assert response.get_json()['status'] == 'success'

def test_analyse_missing_text(client):
    payload = {"wrong key": "This should fail"}
    response = client.post('/api/sentiment/analyse', json=payload)
    assert response.status_code == 400
    assert "error" in response.get_json()