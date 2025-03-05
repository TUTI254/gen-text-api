from repositories.text_repository import TextRepository
from utils.providers.ai_provider_factory import AIProviderFactory
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

class TextService:
    @staticmethod
    def generate_text(user_id: int, prompt: str, provider: str = "gemini"):
        if not isinstance(prompt, str) or not prompt.strip():
            logger.debug("Text generation failed: invalid prompt")
            return {"error": "Prompt must be a non-empty string"}, 422

        try:
            provider_instance = AIProviderFactory.get_provider(provider)
            ai_response = provider_instance.generate_text(prompt)
            generated_text = TextRepository.create_text(user_id, prompt, ai_response)
            logger.info(f"Generated text saved for user_id {user_id} with text id {generated_text.id}")
            return {
                "id": generated_text.id,
                "prompt": prompt,
                "response": ai_response,
                "timestamp": generated_text.timestamp
            }, 201
        except Exception as e:
            logger.exception("Unexpected error in generate_text")
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def get_generated_text(text_id: int, user_id: int):
        try:
            generated_text = TextRepository.get_text_by_id(text_id, user_id)
            if not generated_text:
                logger.debug(f"Text not found for text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            return {
                "id": generated_text.id,
                "prompt": generated_text.prompt,
                "response": generated_text.response,
                "timestamp": generated_text.timestamp
            }, 200
        except Exception as e:
            logger.exception("Unexpected error in get_generated_text")
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def update_generated_text(text_id: int, user_id: int, new_response: str):
        if not isinstance(new_response, str) or not new_response.strip():
            logger.debug("Update generated text failed: invalid new_response")
            return {"error": "New response must be a non-empty string"}, 422

        try:
            generated_text = TextRepository.get_text_by_id(text_id, user_id)
            if not generated_text:
                logger.debug(f"Text not found for update: text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            updated_text = TextRepository.update_text(generated_text, new_response)
            logger.info(f"Text updated successfully for text_id {text_id}")
            return {"message": "Text updated successfully"}, 200
        except SQLAlchemyError as e:
            logger.exception("SQLAlchemyError in update_generated_text")
            return {"error": f"Database error: {str(e)}"}, 500

    @staticmethod
    def delete_generated_text(text_id: int, user_id: int):
        try:
            generated_text = TextRepository.get_text_by_id(text_id, user_id)
            if not generated_text:
                logger.debug(f"Text not found for delete: text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            TextRepository.delete_text(generated_text)
            logger.info(f"Text deleted successfully for text_id {text_id}")
            return {"message": "Text deleted successfully"}, 200
        except SQLAlchemyError as e:
            logger.exception("SQLAlchemyError in delete_generated_text")
            return {"error": f"Database error: {str(e)}"}, 500
