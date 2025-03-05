import pytest
from database import db
from models.generated_text import GeneratedText
from repositories.text_repository import TextRepository
from repositories.user_repository import UserRepository

def create_sample_user():
    return UserRepository.create_user("sampleuser", "samplepass")

def test_create_get_update_delete_text(app_fixture):
    user = create_sample_user()

    # Create a GeneratedText record
    gen_text = TextRepository.create_text(user.id, "Test prompt", "Initial response")
    assert gen_text.id is not None
    assert gen_text.prompt == "Test prompt"

    # Retrieve the record
    found_text = TextRepository.get_text_by_id(gen_text.id, user.id)
    assert found_text is not None
    assert found_text.response == "Initial response"

    # Update the text record
    updated_text = TextRepository.update_text(found_text, "Updated response")
    assert updated_text.response == "Updated response"

    # Delete the record and verify deletion
    TextRepository.delete_text(updated_text)
    deleted_text = TextRepository.get_text_by_id(gen_text.id, user.id)
    assert deleted_text is None
