import pytest
from services.auth_service import AuthService
from repositories.user_repository import UserRepository

def test_auth_service_register_and_login(app_fixture):
    # Register a new user (username will be normalized to lowercase)
    response, status = AuthService.register_user("TestUser", "testpass")
    assert status == 201
    assert response.get("message") == "User registered successfully"
    
    # Attempt duplicate registration
    response, status = AuthService.register_user("TestUser", "testpass")
    assert status == 400
    assert "error" in response

    # Login with correct credentials
    response, status = AuthService.login_user("TestUser", "testpass")
    assert status == 200
    assert "access_token" in response

    # Login with incorrect password
    response, status = AuthService.login_user("TestUser", "wrongpass")
    assert status == 401
    assert "error" in response
