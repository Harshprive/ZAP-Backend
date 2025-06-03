from flask import Blueprint, request, jsonify
from flask import Blueprint, request, jsonify
from bson import ObjectId
from app.extensions import mongo, fs
from datetime import datetime
from io import BytesIO
from app.services.provider_service import (
    register_provider,
    login_provider,
    upload_documents,
    upload_professional_documents,
    set_services,
    set_appointment,
    update_location_for_provider,
    get_provider_requests,
    update_duty_status,
    accept_or_reject_request
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
@provider_bp.route("/location", methods=["POST"])
@jwt_required()
def update_provider_location():
    provider_id = get_jwt_identity()  # This should be the JWT 'sub'
    data = request.get_json()

    latitude = data.get("latitude")
    longitude = data.get("longitude")

    if latitude is None or longitude is None:
        return {"msg": "Latitude and Longitude required"}, 400

    result = update_location_for_provider(provider_id, latitude, longitude)
    return result
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



from flask import Blueprint, jsonify, request, send_file



@provider_bp.route("/dashboard", methods=["GET"])
@jwt_required()
def provider_dashboard():
    provider_id = get_jwt_identity()
    data = get_provider_requests(provider_id)
    return jsonify(data), 200


@provider_bp.route("/duty", methods=["POST"])
@jwt_required()
def update_duty():
    provider_id = get_jwt_identity()
    status = request.json.get("status")
    return update_duty_status(provider_id, status)


@provider_bp.route("/request/<request_id>/<action>", methods=["POST"])
@jwt_required()
def update_request_status(request_id, action):
    provider_id = get_jwt_identity()
    return accept_or_reject_request(provider_id, request_id, action)


@provider_bp.route("/attachment/<file_id>", methods=["GET"])
@jwt_required()
def get_attachment(file_id):

    file = fs.get(ObjectId(file_id))
    return send_file(BytesIO(file.read()), mimetype=file.content_type, download_name=file.filename)
