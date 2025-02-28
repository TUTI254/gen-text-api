from database import db
from sqlalchemy.sql import func

class GeneratedText(db.Model):
    __tablename__ = 'generated_texts'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=func.now())

    user = db.relationship('User', backref=db.backref('generated_texts', lazy=True))
