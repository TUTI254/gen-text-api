import pytest
from flask_jwt_extended import create_access_token

def test_generate_text_missing_prompt(client):
    # First, register and log in to get a valid token
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    cookies = login_response.headers.get_all("Set-Cookie")
    cookie_str = "; ".join(cookies)

    response = client.post("/api/text/generate-text", json={}, headers={"Cookie": cookie_str})
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data

def test_generate_text_success(client, monkeypatch):
    # Patch the AI provider to return a fake response
    class FakeProvider:
        def generate_text(self, prompt):
            return "Fake AI response"

    monkeypatch.setattr(
        "utils.providers.ai_provider_factory.AIProviderFactory.get_provider",
        lambda provider: FakeProvider()
    )

    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    cookies = login_response.headers.get_all("Set-Cookie")
    cookie_str = "; ".join(cookies)

    response = client.post("/api/text/generate-text", json={"prompt": "Hello, AI!"}, headers={"Cookie": cookie_str})
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("prompt") == "Hello, AI!"
    assert data.get("response") == "Fake AI response"
