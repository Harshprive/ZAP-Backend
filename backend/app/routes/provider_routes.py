from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.extensions import mongo, fs
from datetime import datetime

from app.services.provider_service import (
    register_provider,
    login_provider,
    upload_documents,
    upload_professional_documents,
    set_services,
    set_appointment
)
from flask_jwt_extended import jwt_required, get_jwt_identity

provider_bp = Blueprint("provider", __name__)

@provider_bp.route("/register", methods=["POST"])
def register():
    data = request.json
    return register_provider(data)

@provider_bp.route("/login", methods=["POST"])
def login():
    data = request.json
    return login_provider(data)

@provider_bp.route("/upload-documents", methods=["POST"])
@jwt_required()
def upload_docs():
    provider_id = get_jwt_identity()
    if 'aadhaar' not in request.files or 'pan' not in request.files or 'selfie' not in request.files:
        return {"msg": "Missing required files"}, 400

    files = {
        "aadhaar": request.files['aadhaar'],
        "pan": request.files['pan'],
        "selfie": request.files['selfie']
    }

    return upload_documents(provider_id, files)


@provider_bp.route("/professional-documents", methods=["POST"])
@jwt_required()
def upload_pro_docs():
    provider_id = get_jwt_identity()
    data = request.json
    return upload_professional_documents(provider_id, data)

@provider_bp.route("/set-services", methods=["POST"])
@jwt_required()
def set_service():
    provider_id = get_jwt_identity()
    data = request.json
    return set_services(provider_id, data)

@provider_bp.route("/set-appointment", methods=["POST"])
@jwt_required()
def appointment():
    provider_id = get_jwt_identity()
    data = request.json
    return set_appointment(provider_id, data)
