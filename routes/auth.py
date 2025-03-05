from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, set_access_cookies,unset_jwt_cookies
from services.auth_service import AuthService
import logging

logger = logging.getLogger(__name__)

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.debug("Register validation failed: missing username or password")
        return {"error": "Username and password are required"}, 422

    return AuthService.register_user(username, password)

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if not username or not password:
        logger.debug("Login validation failed: missing username or password")
        return {"error": "Username and password are required"}, 422

    result, status_code = AuthService.login_user(username, password)

    if status_code != 200:
        return result, status_code

    # Retrieve the access token from the result
    access_token = result.get("access_token")
    # Create a response and set the JWT in a secure cookie
    response = make_response(jsonify({"message": "Login successful"}), 200)
    set_access_cookies(response, access_token)
    return response

@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    response = make_response(jsonify({"message": "Logout successful"}), 200)
    unset_jwt_cookies(response)
    return response