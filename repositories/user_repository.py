from models.user import User
from database import db

class UserRepository:
    @staticmethod
    def get_user_by_username(username: str):
        return User.query.filter_by(username=username).first()

    @staticmethod
    def create_user(username: str, password: str) -> User:
        user = User(username=username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        return user
