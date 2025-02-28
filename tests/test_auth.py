import json

def test_register_user(client):
    """Test user registration"""
    response = client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert "message" in data

def test_login_user(client):
    """Test user login"""
    client.post("/api/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    
    response = client.post("/api/auth/login", json={
        "email": "test@example.com",
        "password": "password123"
    })
    assert response.status_code == 200
    data = response.get_json()
    assert "access_token" in data
