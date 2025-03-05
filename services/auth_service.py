from models.user import User
from database import db
from flask_jwt_extended import create_access_token
from datetime import timedelta

class AuthService:
    @staticmethod
    def register_user(username, password):
        """Registers a new user"""
        normalized_username = username.lower()
        if User.query.filter_by(username=normalized_username).first():
            return {"error": "User already exists"}, 400
        
        user = User(username=normalized_username)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        return {"message": "User registered successfully"}, 201

    @staticmethod
    def login_user(username, password):
        """Authenticates and returns a JWT token"""
        normalized_username = username.lower()
        user = User.query.filter_by(username=normalized_username).first()
        
        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401
        
        access_token = create_access_token(identity=str(user.id), expires_delta=timedelta(hours=2))
        return {"access_token": access_token}, 200
