import pytest
from app import create_app
from database import db
from config import TestConfig

@pytest.fixture
def app_fixture():
    """Return app with an application context for testing."""
    app = create_app(TestConfig)
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app_fixture):
    """Set up test client using the app_fixture."""
    return app_fixture.test_client()
