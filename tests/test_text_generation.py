import json

def test_generate_text(client):
    """Test AI text generation"""
    # Register & Login User
    client.post("/api/auth/register", json={"email": "user@example.com", "password": "test123"})
    login_response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "test123"})
    token = login_response.get_json()["access_token"]

    # Generate AI text
    response = client.post("/api/text/generate-text",
        headers={"Authorization": f"Bearer {token}"},
        json={"prompt": "Tell me a joke"}
    )

    assert response.status_code == 201
    data = response.get_json()
    assert "response" in data

def test_get_generated_text(client):
    """Test retrieving AI-generated text"""
    client.post("/api/auth/register", json={"email": "user@example.com", "password": "test123"})
    login_response = client.post("/api/auth/login", json={"email": "user@example.com", "password": "test123"})
    token = login_response.get_json()["access_token"]

    # Generate AI text
    gen_response = client.post("/api/text/generate-text",
        headers={"Authorization": f"Bearer {token}"},
        json={"prompt": "Tell me a joke"}
    )
    text_id = gen_response.get_json()["id"]

    # Retrieve the generated text
    response = client.get(f"/api/text/generated-text/{text_id}",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    data = response.get_json()
    assert "response" in data
