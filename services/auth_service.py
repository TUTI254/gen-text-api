from repositories.user_repository import UserRepository
from flask_jwt_extended import create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def register_user(username, password):
        normalized_username = username.lower()
        if UserRepository.get_user_by_username(normalized_username):
            logger.debug(f"Registration attempt for existing user: {normalized_username}")
            return {"error": "User already exists"}, 400
        try:
            UserRepository.create_user(normalized_username, password)
            logger.info(f"User registered successfully: {normalized_username}")
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            logger.exception("Error during user registration")
            return {"error": f"Registration failed: {str(e)}"}, 500

    @staticmethod
    def login_user(username, password):
        normalized_username = username.lower()
        user = UserRepository.get_user_by_username(normalized_username)
        if not user or not user.check_password(password):
            logger.debug(f"Invalid login attempt for user: {normalized_username}")
            return {"error": "Invalid credentials"}, 401
        try:
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=2))
            logger.info(f"User logged in successfully: {normalized_username}")
            return {"access_token": access_token}, 200
        except Exception as e:
            logger.exception("Error during login")
            return {"error": f"Login failed: {str(e)}"}, 500
