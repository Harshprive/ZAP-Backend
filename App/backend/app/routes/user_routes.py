from flask import Blueprint, request, jsonify
from app.services.user_service import register_user ,login_user

user_bp = Blueprint("user", __name__)

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    result, code = login_user(data)
    return jsonify(result), code