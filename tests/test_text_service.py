import pytest
from services.text_service import TextService
from models.generated_text import GeneratedText

# Create a fake provider to simulate AI text generation.
class FakeProvider:
    def generate_text(self, prompt):
        return "Fake AI response"

@pytest.fixture
def fake_provider(monkeypatch):
    from utils.providers.ai_provider_factory import AIProviderFactory
    monkeypatch.setattr(AIProviderFactory, "get_provider", lambda provider: FakeProvider())
    return True

def test_generate_text_invalid_prompt(app_fixture, fake_provider):
    # Test with an invalid (empty) prompt
    response, status = TextService.generate_text(user_id=1, prompt="   ")
    assert status in (422, 400)
    assert "error" in response

def test_generate_text_success(app_fixture, fake_provider):
    response, status = TextService.generate_text(user_id=1, prompt="Hello, AI!")
    assert status == 201
    assert response.get("prompt") == "Hello, AI!"
    assert response.get("response") == "Fake AI response"
    # Verify the generated record exists in the database
    gen_text = GeneratedText.query.get(response.get("id"))
    assert gen_text is not None

def test_get_generated_text_not_found(app_fixture):
    response, status = TextService.get_generated_text(text_id=999, user_id=1)
    assert status == 404
    assert "error" in response

def test_update_generated_text_invalid(app_fixture):
    # Create a generated text record directly
    from repositories.text_repository import TextRepository
    gen_text = TextRepository.create_text(1, "Test Prompt", "Old Response")
    response, status = TextService.update_generated_text(text_id=gen_text.id, user_id=1, new_response="   ")
    assert status in (422, 400)
    assert "error" in response

def test_delete_generated_text_not_found(app_fixture):
    response, status = TextService.delete_generated_text(text_id=999, user_id=1)
    assert status == 404
    assert "error" in response
