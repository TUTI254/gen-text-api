import pytest

def test_register_missing_fields(client):
    # Missing password
    response = client.post("/api/auth/register", json={"username": "testuser"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

    # Missing username
    response = client.post("/api/auth/register", json={"password": "testpass"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_register_success(client):
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 201
    data = response.get_json()
    assert data.get("message") == "User registered successfully"

def test_register_duplicate(client):
    # Register the user once
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    # Attempt to register the same user again
    response = client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_login_missing_fields(client):
    response = client.post("/api/auth/login", json={"username": "testuser"})  # missing password
    assert response.status_code == 400
    data = response.get_json()
    assert "error" in data

def test_login_invalid_credentials(client):
    # No user exists with these credentials
    response = client.post("/api/auth/login", json={"username": "nonexistent", "password": "wrongpass"})
    assert response.status_code == 401
    data = response.get_json()
    assert "error" in data

def test_login_success(client):
    # First register a user
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    assert response.status_code == 200
    data = response.get_json()
    assert data.get("message") == "Login successful"
    # Check that the JWT cookie is set 
    cookie_header = response.headers.get("Set-Cookie")
    assert cookie_header is not None
    assert "access_token_cookie" in cookie_header

def test_logout_without_token(client):
    # Without a valid JWT, the endpoint should return an error
    response = client.post("/api/auth/logout")
    assert response.status_code in (401, 422)

def test_logout_success(client):
    # Register and log in to get a valid JWT cookie
    client.post("/api/auth/register", json={"username": "testuser", "password": "testpass"})
    login_response = client.post("/api/auth/login", json={"username": "testuser", "password": "testpass"})
    # Extract cookies from the login response
    cookies = login_response.headers.get_all("Set-Cookie")
    cookie_str = "; ".join(cookies)
    # Use the cookie in the logout request header
    logout_response = client.post("/api/auth/logout", headers={"Cookie": cookie_str})
    assert logout_response.status_code == 200
    data = logout_response.get_json()
    assert data.get("message") == "Logout successful"
