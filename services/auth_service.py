from models.user import User
from database import db
from flask_jwt_extended import create_access_token
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

class AuthService:
    @staticmethod
    def register_user(username, password):
        """Registers a new user"""
        normalized_username = username.lower()
        if User.query.filter_by(username=normalized_username).first():
            logger.debug(f"Registration attempt for existing user: {normalized_username}")
            return {"error": "User already exists"}, 400
        
        try:
            user = User(username=normalized_username)
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            logger.info(f"User registered successfully: {normalized_username}")
            return {"message": "User registered successfully"}, 201
        except Exception as e:
            logger.exception("Error during user registration")
            db.session.rollback()
            return {"error": f"Registration failed: {str(e)}"}, 500

    @staticmethod
    def login_user(username, password):
        """Authenticates and returns a JWT token"""
        normalized_username = username.lower()
        user = User.query.filter_by(username=normalized_username).first()
        
        try:
            access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=2))
            logger.info(f"User logged in successfully: {normalized_username}")
            return {"access_token": access_token}, 200
        except Exception as e:
            logger.exception("Error during login")
            return {"error": f"Login failed: {str(e)}"}, 500
