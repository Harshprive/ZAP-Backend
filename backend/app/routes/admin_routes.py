from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt
from app.services.admin_service import fetch_logs

admin_bp = Blueprint("admin", __name__)

@admin_bp.route("/logs", methods=["GET"])
@jwt_required()
def get_logs():
    claims = get_jwt()
    if claims.get("role") != "admin":
        return {"msg": "Admins only"}, 403
    return jsonify(fetch_logs())
