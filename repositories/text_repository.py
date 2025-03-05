from models.generated_text import GeneratedText
from database import db

class TextRepository:
    @staticmethod
    def create_text(user_id: int, prompt: str, response: str) -> GeneratedText:
        text = GeneratedText(user_id=user_id, prompt=prompt, response=response)
        db.session.add(text)
        db.session.commit()
        return text

    @staticmethod
    def get_text_by_id(text_id: int, user_id: int) -> GeneratedText:
        return GeneratedText.query.filter_by(id=text_id, user_id=user_id).first()

    @staticmethod
    def update_text(text: GeneratedText, new_response: str) -> GeneratedText:
        text.response = new_response
        db.session.commit()
        return text

    @staticmethod
    def delete_text(text: GeneratedText) -> None:
        db.session.delete(text)
        db.session.commit()
