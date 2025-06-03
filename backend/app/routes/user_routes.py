# app/routes/user_routes.py

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.user_service import (
    register_user, login_user, update_location, save_preferences,
    get_user_by_id, get_services, search_services,
    get_recommended_services, get_map_data,find_service_for_user
)
from flask_jwt_extended import jwt_required, get_jwt_identity



user_bp = Blueprint("user_bp", __name__, url_prefix="/api/user")

@user_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_user(data)

@user_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_user(data)

@user_bp.route("/location", methods=["POST"])
@jwt_required()
def update_user_location_route():
    user_id = get_jwt_identity()
    data = request.json
    return update_location(user_id, data)

@user_bp.route("/preferences", methods=["POST"])
@jwt_required()
def save_service_preferences():
    user_id = get_jwt_identity()
    data = request.json
    return save_preferences(user_id, data)

@user_bp.route("/me", methods=["GET"])
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = get_user_by_id(user_id)
    if not user:
        return {"msg": "User not found"}, 404
    user["_id"] = str(user["_id"])
    return jsonify(user), 200

@user_bp.route("/services", methods=["GET"])
def services():
    return jsonify(get_services())

@user_bp.route("/search", methods=["GET"])
def search():
    query = request.args.get("q", "")
    return jsonify(search_services(query))

@user_bp.route("/recommendations", methods=["GET"])
@jwt_required()
def recommendations():
    return jsonify(get_recommended_services())

@user_bp.route("/map-data", methods=["GET"])
def map_data():
    return jsonify(get_map_data())

from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from bson import ObjectId

@user_bp.route("/find-now", methods=["POST"])
@jwt_required()
def find_now():
    user_id = get_jwt_identity()
    data = request.get_json()
    data["user_id"] = user_id
    return find_service_for_user(data)  # ✅ Remove jsonify() here
