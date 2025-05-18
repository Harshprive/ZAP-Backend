from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.matching_service import match_user_with_providers

matching_bp = Blueprint("matching", __name__)

@matching_bp.route("/request", methods=["POST"])
@jwt_required()
def request_service():
    data = request.json
    user_id = get_jwt_identity()
    return match_user_with_providers(user_id, data["service"])
