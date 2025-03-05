import pytest
from database import db
from models.user import User
from repositories.user_repository import UserRepository

def test_create_and_get_user(app_fixture):
    # Initially, the user should not exist
    user = UserRepository.get_user_by_username("testuser")
    assert user is None

    # Create a new user
    new_user = UserRepository.create_user("testuser", "testpass")
    assert new_user.username == "testuser"

    # Now the user should be retrievable
    found_user = UserRepository.get_user_by_username("testuser")
    assert found_user is not None
    assert found_user.id == new_user.id

def test_get_nonexistent_user(app_fixture):
    user = UserRepository.get_user_by_username("nonexistent")
    assert user is None
