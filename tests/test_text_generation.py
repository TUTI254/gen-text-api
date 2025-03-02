import pytest
from services.text_service import TextService, client
from models.generated_text import GeneratedText
from database import db

# A fake completion object to simulate the OpenAI response
class FakeCompletion:
    class FakeChoice:
        message = type("FakeMessage", (), {"content": "Fake AI response"})
    choices = [FakeChoice()]

def fake_create(*args, **kwargs):
    return FakeCompletion()

@pytest.fixture(autouse=True)
def patch_openai(monkeypatch):
    # Patch the OpenAI client's chat.completions.create method to use our fake_create
    monkeypatch.setattr(client.chat.completions, "create", fake_create)

def test_generate_text_invalid_prompt(app_fixture):
    # Test with an invalid (empty) prompt
    response, status = TextService.generate_text(user_id=1, prompt="   ")
    assert status == 400
    assert "error" in response

def test_generate_text_success(app_fixture):
    # Test generating text with a valid prompt
    response, status = TextService.generate_text(user_id=1, prompt="Hello, AI!")
    assert status == 201
    assert response.get("prompt") == "Hello, AI!"
    assert response.get("response") == "Fake AI response"
    # Confirm the generated text is saved in the database
    generated_text = GeneratedText.query.get(response.get("id"))
    assert generated_text is not None
    assert generated_text.response == "Fake AI response"

def test_get_generated_text_not_found(app_fixture):
    response, status = TextService.get_generated_text(text_id=999, user_id=1)
    assert status == 404
    assert "error" in response

def test_get_generated_text_success(app_fixture):
    # Create a GeneratedText record directly
    new_text = GeneratedText(user_id=1, prompt="Test Prompt", response="Test Response")
    db.session.add(new_text)
    db.session.commit()

    response, status = TextService.get_generated_text(text_id=new_text.id, user_id=1)
    assert status == 200
    assert response.get("id") == new_text.id

def test_update_generated_text_invalid_new_response(app_fixture):
    new_text = GeneratedText(user_id=1, prompt="Test Prompt", response="Old Response")
    db.session.add(new_text)
    db.session.commit()

    response, status = TextService.update_generated_text(text_id=new_text.id, user_id=1, new_response="   ")
    assert status == 400
    assert "error" in response

def test_update_generated_text_not_found(app_fixture):
    response, status = TextService.update_generated_text(text_id=999, user_id=1, new_response="New Response")
    assert status == 404
    assert "error" in response

def test_update_generated_text_success(app_fixture):
    new_text = GeneratedText(user_id=1, prompt="Test Prompt", response="Old Response")
    db.session.add(new_text)
    db.session.commit()

    response, status = TextService.update_generated_text(text_id=new_text.id, user_id=1, new_response="New Response")
    assert status == 200
    assert response.get("message") == "Text updated successfully"
    # Verify update in the database
    updated_text = GeneratedText.query.get(new_text.id)
    assert updated_text.response == "New Response"

def test_delete_generated_text_not_found(app_fixture):
    response, status = TextService.delete_generated_text(text_id=999, user_id=1)
    assert status == 404
    assert "error" in response

def test_delete_generated_text_success(app_fixture):
    new_text = GeneratedText(user_id=1, prompt="Test Prompt", response="Test Response")
    db.session.add(new_text)
    db.session.commit()

    response, status = TextService.delete_generated_text(text_id=new_text.id, user_id=1)
    assert status == 200
    assert response.get("message") == "Text deleted successfully"
    # Verify the text was removed from the database
    deleted_text = GeneratedText.query.get(new_text.id)
    assert deleted_text is None
