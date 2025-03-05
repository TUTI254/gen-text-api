import pytest

def test_register_missing_fields(client):
    # Missing password
    response = client.post("/api/auth/register", json={"username": "testuser"})
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data

    # Missing username
    response = client.post("/api/auth/register", json={"password": "testpass"})
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data

def test_register_success(client):
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("message") == "User registered successfully"

def test_register_duplicate(client):
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={"username": "testuser"})
    assert response.status_code == 422
    data = response.get_json()
    assert "error" in data

def test_login_invalid_credentials(client):
    response = client.post("/api/auth/login", json={"username": "nonexistent", "password": "wrongpass"})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_login_success(client):
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    # Check that the JWT cookie is set
    cookie_header = response.headers.get("Set-Cookie")
    assert cookie_header is not None
    assert "access_token_cookie" in cookie_header

def test_logout_without_token(client):
    response = client.post("/api/auth/logout")
    assert response.status_code in (401, 422)

def test_logout_success(client):
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    cookies = login_response.headers.get_all("Set-Cookie")
    cookie_str = "; ".join(cookies)
    logout_response = client.post("/api/auth/logout", headers={"Cookie": cookie_str})
    assert logout_response.status_code == 200
    data = logout_response.get_json()
    assert data.get("message") == "Logout successful"
