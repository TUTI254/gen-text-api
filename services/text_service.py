import os
from openai import OpenAI
from database import db
from models.generated_text import GeneratedText
from sqlalchemy.exc import SQLAlchemyError

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


class TextService:
    @staticmethod
    def generate_text(user_id: int, prompt: str):
        """Generates AI text from OpenAI API and saves it"""
        if not isinstance(prompt, str) or not prompt.strip():
            return {"error": "Prompt must be a non-empty string"}, 400

        try:
            user_id = int(user_id)

            completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant."},
                    {"role": "user", "content": prompt}
                ]
            )

            ai_response = completion.choices[0].message.content

            # Save generated response to database
            generated_text = GeneratedText(user_id=user_id, prompt=prompt, response=ai_response)
            db.session.add(generated_text)
            db.session.commit()

            return {
                "id": generated_text.id,
                "prompt": prompt,
                "response": ai_response,
                "timestamp": generated_text.timestamp
            }, 201

        except ValueError:
            return {"error": "Invalid user_id format"}, 400
        except Exception as e:
            return {"error": f"Unexpected error: {str(e)}"}, 500

    @staticmethod
    def get_generated_text(text_id: int, user_id: int):
        """Retrieve an AI-generated text by ID"""
        try:
            user_id = int(user_id)
            text_id = int(text_id)

            generated_text = GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()
            if not generated_text:
                return {"error": "Text not found"}, 404

            return {
                "id": generated_text.id,
                "prompt": generated_text.prompt,
                "response": generated_text.response,
                "timestamp": generated_text.timestamp
            }, 200

        except ValueError:
            return {"error": "Invalid user_id or text_id format"}, 400
        except Exception as e:
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
                return {"error": "Text not found"}, 404

            generated_text.response = new_response

            db.session.commit()
            return {"message": "Text updated successfully"}, 200

        except ValueError:
            return {"error": "Invalid user_id or text_id format"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500

    @staticmethod
    def delete_generated_text(text_id: int, user_id: int):
        """Delete an AI-generated text"""
        try:
            user_id = int(user_id)
            text_id = int(text_id)

            generated_text = GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()
            if not generated_text:
                return {"error": "Text not found"}, 404

            db.session.delete(generated_text)
            db.session.commit()
            return {"message": "Text deleted successfully"}, 200

        except ValueError:
            return {"error": "Invalid user_id or text_id format"}, 400
        except SQLAlchemyError as e:
            db.session.rollback()
            return {"error": f"Database error: {str(e)}"}, 500
        