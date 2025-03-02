# tests/test_models.py
from database import db
from models.user import User
from models.generated_text import GeneratedText

def test_user_creation(app_fixture):
    """
    Test creating a User and verifying password functionality.
    """
    # Create a new user
    user = User(username="testuser")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Query the user from the database
    queried_user = User.query.filter_by(username="testuser").first()
    assert queried_user is not None
    assert queried_user.username == "testuser"
    
    # Verify password checking works
    assert queried_user.check_password("testpassword") is True
    assert queried_user.check_password("wrongpassword") is False

def test_generated_text_creation(app_fixture):
    """
    Test creating a GeneratedText record linked to a User.
    """
    # Create a new user first
    user = User(username="testuser")
    user.set_password("testpassword")
    db.session.add(user)
    db.session.commit()

    # Create a GeneratedText record for the user
    gen_text = GeneratedText(
        user_id=user.id,
        prompt="Tell me something funny",
        response="Here's a joke for you!"
    )
    db.session.add(gen_text)
    db.session.commit()

    # Query the generated text record
    queried_text = GeneratedText.query.filter_by(user_id=user.id).first()
    assert queried_text is not None
    assert queried_text.prompt == "Tell me something funny"
    assert queried_text.response == "Here's a joke for you!"

    # Verify that the relationship returns the correct user
    assert queried_text.user.username == "testuser"
