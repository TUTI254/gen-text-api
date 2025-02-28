from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from services.text_service import TextService

text_bp = Blueprint("text", __name__, url_prefix="/api/text")

@text_bp.route("/generate-text", methods=["POST"])
@jwt_required()
def generate_text():
    """Generate AI-powered text"""
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        return {"error": "Prompt is required"}, 400

    user_id = get_jwt_identity()
    return TextService.generate_text(user_id, prompt)

@text_bp.route("/generated-text/<int:text_id>", methods=["GET"])
@jwt_required()
def get_text(text_id):
    """Retrieve AI-generated text by ID"""
    user_id = get_jwt_identity()
    return TextService.get_generated_text(text_id, user_id)

@text_bp.route("/generated-text/<int:text_id>", methods=["PUT"])
@jwt_required()
def update_text(text_id):
    """Update stored AI-generated text"""
    data = request.get_json()
    new_response = data.get("response")

    if not new_response:
        return {"error": "Updated response is required"}, 400

    user_id = get_jwt_identity()
    return TextService.update_generated_text(text_id, user_id, new_response)

@text_bp.route("/generated-text/<int:text_id>", methods=["DELETE"])
@jwt_required()
def delete_text(text_id):
    """Delete AI-generated text"""
    user_id = get_jwt_identity()
    return TextService.delete_generated_text(text_id, user_id)
