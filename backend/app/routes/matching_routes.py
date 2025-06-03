from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.matching_service import match_user_with_providers





matching_bp = Blueprint("matching_bp", __name__)

@matching_bp.route("/find-now", methods=["POST"])
@jwt_required()
def find_now():
    user_id = get_jwt_identity()
    data = request.get_json()
    service = data.get("service")

    if not service:
        return jsonify({"msg": "Service is required"}), 400

    result, status = match_user_with_providers(user_id, service)
    return jsonify(result), status
