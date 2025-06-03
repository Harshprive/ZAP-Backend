from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.issue_service import submit_issue
from bson import ObjectId

issue_bp = Blueprint("issue_bp", __name__)

@issue_bp.route("/issue", methods=["POST"])
@jwt_required()
def post_issue():
    user_id = get_jwt_identity()
    json_data = request.form  # JSON part from form-data
    file = request.files.get("file")  # File part

    if not json_data.get("issue") or not json_data.get("min_days"):
        return jsonify({"msg": "Missing required fields"}), 400

    result = submit_issue(user_id, json_data, file)
    return jsonify(result), 201
