import pytest
from app import app
from database import db
from config import TestConfig

@pytest.fixture
def client():
    """Set up test client and database."""
    app.config.from_object(TestConfig)
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()
