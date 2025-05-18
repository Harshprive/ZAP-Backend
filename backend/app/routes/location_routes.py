from flask import Blueprint, request, jsonify
from app.services.location_service import add_location

location_bp = Blueprint("location", __name__)

@location_bp.route("/add", methods=["POST"])
def add_location_route():
    data = request.json
    result, code = add_location(data)
    return jsonify(result), code
