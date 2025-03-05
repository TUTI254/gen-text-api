from database import db
from models.generated_text import GeneratedText
from sqlalchemy.exc import SQLAlchemyError
from utils.providers.ai_provider_factory import AIProviderFactory
import logging

logger = logging.getLogger(__name__)

class TextService:
    @staticmethod
    def generate_text(user_id: int, prompt: str, provider: str = "gemini"):
        """Generates AI text using the specified provider and saves it."""
        if not isinstance(prompt, str) or not prompt.strip():
            logger.debug("Text generation failed: invalid prompt")
            return {"error": "Prompt must be a non-empty string"}, 422

        try:
            user_id = int(user_id)

            # Create the provider instance based on the given provider name.
            provider_instance = AIProviderFactory.get_provider(provider)
            ai_response = provider_instance.generate_text(prompt)

            # Save generated response to database
            generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=ai_response)
            db.session.add(generated_text)
            db.session.commit()
            logger.info(f"Generated text saved for user_id {user_id} with text id {generated_text.id}")

            return {
                "id": generated_text.id,
                "prompt": prompt,
                "response": ai_response,
                "timestamp": generated_text.timestamp
            }, 201

        except ValueError as ve:
            logger.exception("ValueError in generate_text")
            return {"error": str(ve)}, 400
        except Exception as e:
            logger.exception("Unexpected error in generate_text")
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def get_generated_text(text_id: int, user_id: int):
        """Retrieve an AI-generated text by ID"""
        try:
            user_id = int(user_id)
            text_id = int(text_id)

            generated_text = GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()
            if not generated_text:
                logger.debug(f"Text not found for text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            return {
                "id": generated_text.id,
                "prompt": generated_text.prompt,
                "response": generated_text.response,
                "timestamp": generated_text.timestamp
            }, 200

        except ValueError:
            logger.exception("ValueError in get_generated_text")
            return {"error": "Invalid user_id or text_id format"}, 400
        except Exception as e:
            logger.exception("Unexpected error in get_generated_text")
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def update_generated_text(text_id: int, user_id: int, new_response: str):
        """Update an AI-generated text response"""
        if not isinstance(new_response, str) or not new_response.strip():
            return {"error": "New response must be a non-empty string"}, 400

        try:
            user_id = int(user_id)
            text_id = int(text_id)

            generated_text = GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()
            if not generated_text:
                logger.debug(f"Text not found for update: text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            generated_text.response = new_response
            db.session.commit()
            logger.info(f"Text updated successfully for text_id {text_id}")
            return {"message": "Text updated successfully"}, 200

        except ValueError:
            logger.exception("ValueError in update_generated_text")
            return {"error": "Invalid user_id or text_id format"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            logger.exception("SQLAlchemyError in update_generated_text")
            return {"error": f"Database error: {str(e)}"}, 500

    @staticmethod
    def delete_generated_text(text_id: int, user_id: int):
        """Delete an AI-generated text"""
        try:
            user_id = int(user_id)
            text_id = int(text_id)

            generated_text = GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()
            if not generated_text:
                logger.debug(f"Text not found for delete: text_id {text_id} and user_id {user_id}")
                return {"error": "Text not found"}, 404

            db.session.delete(generated_text)
            db.session.commit()
            logger.info(f"Text deleted successfully for text_id {text_id}")
            return {"message": "Text deleted successfully"}, 200

        except ValueError:
            logger.exception("ValueError in delete_generated_text")
            return {"error": "Invalid user_id or text_id format"}, 400
        except SQLAlchemyError as e:
            logger.exception("SQLAlchemyError in delete_generated_text")
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500
