from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from services.text_service import TextService
import logging


logger = logging.getLogger(__name__)

text_bp = Blueprint("text", __name__, url_prefix="/api/text")
limiter = Limiter(key_func=get_remote_address)

@text_bp.route("/generate-text", methods=["POST"])
@jwt_required()
@limiter.limit("5 per minute")
def generate_text():
    """Generate AI-powered text"""
    data = request.get_json()
    prompt = data.get("prompt")
    
    if not prompt:
        logger.debug("Generate text validation failed: missing prompt")
        return {"error": "Prompt is required"}, 422

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
        logger.debug("Update text validation failed: missing updated response")
        return {"error": "Updated response is required"}, 422

    user_id = get_jwt_identity()
    return TextService.update_generated_text(text_id, user_id, new_response)

@text_bp.route("/generated-text/<int:text_id>", methods=["DELETE"])
@jwt_required()
def delete_text(text_id):
    """Delete AI-generated text"""
    user_id = get_jwt_identity()
    return TextService.delete_generated_text(text_id, user_id)
