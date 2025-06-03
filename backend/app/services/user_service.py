# app/services/user_service.py

from flask import jsonify
from werkzeug.security import check_password_hash
from app.extensions import mongo, jwt
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.user_model import *
from datetime import datetime, timedelta
import jwt as jwt_lib
from app.extensions import mongo
from app.utils.location_utils import haversine_distance
from bson import ObjectId
from datetime import datetime
from app.models.schedule_model import schedule_service_request
# JWT_SECRET_KEY = ""  # Use env in prod
def register_user(data):

    if get_user_by_email(data["email"]):
        return {"msg": "User already exists"}, 400

    user = {
        "name": data["name"],
        "email": data["email"],
        "password": generate_password_hash(data["password"]),
        "location": None,
        "preferred_services": [],
        "created_at": datetime.utcnow()
    }
    create_user(user)
    return {"msg": "User registered successfully"}, 201

from app.models.user_model import get_user_by_email

def login_user(data):
    user = get_user_by_email(data["email"])

    if not user or not check_password_hash(user["password"], data["password"]):
        return {"msg": "Invalid credentials"}, 401

    # Generate token with user ID as identity and extra claims
    access_token = create_access_token(
        identity=str(user["_id"]),  # ✅ This will be used as `sub`
        additional_claims={         # ✅ Optional: Other claims
            "email": user["email"],
            "role": "user"
        },
        expires_delta=timedelta(hours=2)
    )

    return {"msg": "Login successful", "token": access_token}, 200

def update_location(user_id, location_data):
    update_user_location(user_id, location_data)
    return {"msg": "Location updated"}, 200

def save_preferences(user_id, services):
    save_user_preferred_services(user_id, services)
    return {"msg": "Preferred services saved"}, 200


from app.models.service_model import services_collection
from app.models.location_model import create_match
from app.utils.location_utils import haversine_distance

def get_services():
    return list(services_collection.find())

def search_services(query):
    return list(services_collection.find({"subcategory": {"$regex": query, "$options": "i"}}))

def get_recommended_services():
    return list(services_collection.find().limit(5))

def get_map_data():
    providers = services_collection.find({}, {"location": 1, "subcategory": 1})
    return [{"lat": p["location"]["lat"], "lng": p["location"]["lng"], "subcategory": p["subcategory"]} for p in providers]



def find_service_for_user(data):
    user_location = data["location"]
    service_needed = data.get("subcategory")

    if not service_needed:
        return jsonify({"msg": "Service is required"}), 400

    # Try to find matching services
    candidates = services_collection.find({"subcategory": service_needed})
    results = []

    for c in candidates:
        dist = haversine_distance(user_location, c["location"])
        if dist <= 10:
            results.append({
                "provider_id": c["provider_id"],
                "distance": dist
            })

    if results:
        match_id = create_match({
            "user_id": data["user_id"],
            "results": results
        })
        return {
            "status": "matched",
            "match_id": str(match_id.inserted_id),
            "providers": results
        }
    else:
        # 🔁 Redirect to scheduling queue logic here
        schedule_result = schedule_service_request({
            "user_id": data["user_id"],
            "subcategory": service_needed,
            "location": user_location,
            "timestamp": datetime.utcnow()
        })

        return {
            "status": "no_match",
            "message": "No provider found nearby. Scheduled your request.",
            "schedule_id": str(schedule_result.inserted_id)
        }
