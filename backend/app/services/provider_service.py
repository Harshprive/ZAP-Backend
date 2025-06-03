from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.extensions import mongo , fs ,jwt
from app.models.provider_model import format_request_for_provider
from app.utils.location_utils import haversine_distance
from flask_jwt_extended import create_access_token
import jwt as jwt_lib
from bson import ObjectId
from app.models.provider_model import get_provider_by_email
from gridfs import GridFS
JWT_SECRET_KEY = "6HPFW3INuRkpko4jGQkp9K98ecvokCZuBRlNi5kxfOI"


# Step 1: Register basic provider details
def register_provider(data):
    providers = mongo.db.providers

    if providers.find_one({"email": data["email"]}):
        return {"msg": "Provider already exists"}, 400

    provider = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "email": data["email"],
        "country": data["country"],
        "password": generate_password_hash(data["password"]),
        "is_verified": False,
        "document_verification": {},
        "professional_documents": {},
        "services": {},
        "appointment": {},
        "available": False,
        "created_at": datetime.utcnow(),
        "location":{}
    }

    providers.insert_one(provider)
    return {"msg": "Provider registered successfully"}, 201

# Step 2: Login
def login_provider(data):
    provider = get_provider_by_email(data["email"])

    if not provider or not check_password_hash(provider["password"], data["password"]):
        return {"msg": "Invalid email or password"}, 401

    access_token = create_access_token(
        identity=str(provider["_id"]),  # ✅ Only string here
        additional_claims={             # ✅ Optional extra claims
            "email": provider["email"],
            "role": "provider"
        },
        expires_delta=timedelta(hours=1)
    )

    return {"msg": "Login successful", "token": access_token}, 200

def update_location_for_provider(provider_id, lat, lon):
    try:
        mongo.db.providers.update_one(
            {"_id": ObjectId(provider_id)},
            {"$set": {
                "location": {
                    "latitude": lat,
                    "longitude": lon
                }
            }}
        )
        return {"msg": "Location updated successfully"}, 200
    except Exception as e:
        return {"msg": f"Error updating location: {str(e)}"}, 500
# Step 3: Upload documents (Aadhaar, PAN, Selfie)
def upload_documents(provider_id, files):
    fs = GridFS(mongo.db)
    uploaded_files = {}

    for key, file in files.items():
        file_id = fs.put(file, filename=file.filename, content_type=file.content_type)
        uploaded_files[key] = str(file_id)

    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {
            "$set": {
                "documents": uploaded_files,
                "documents_uploaded_at": datetime.utcnow(),
                "is_verified": False
            }
        }
    )

    return {"msg": "Documents uploaded", "files": uploaded_files}, 200
    return {"msg": "Documents uploaded successfully", "files": uploaded_files}, 200
# Step 4: Professional documents
def upload_professional_documents(provider_id, data):
    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"professional_documents": data}}
    )
    return {"msg": "Professional documents uploaded successfully"}, 200

# Step 5: Service selection
def set_services(provider_id, data):
    provider_services = data.get("services", [])
    
    # Update provider profile with services
    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"services": provider_services}}
    )
    
    # Automatically insert each service into global "services" table if not already present
    for service_name in provider_services:
        mongo.db.services.update_one(
            {"name": service_name},
            {"$setOnInsert": {"name": service_name, "created_at": datetime.utcnow()}},
            upsert=True
        )

    return {"msg": "Services added and synced to global services table."}, 200

# Step 6: Set appointment
def set_appointment(provider_id, data):
    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"appointment": data, "available": True}}
    )
    return {"msg": "Appointment setup complete"}, 200



from bson import ObjectId
from app.models.provider_model import format_request_for_provider
from app.utils.location_utils import haversine_distance


def get_provider_requests(provider_id):
   
    provider = mongo.db.providers.find_one({"_id": ObjectId(provider_id)})

    if not provider or provider.get("duty_status") != "on":
        return []

    # Fetch only relevant requests for this provider's subcategory
    matching_requests = mongo.db.requests.find({
        "subcategory": {"$in": provider.get("subcategories", [])},
        "status": "Pending"
    })

    results = []

    for req in matching_requests:
        user = mongo.db.users.find_one({"_id": ObjectId(req["user_id"])})

        # Distance & ETA
        distance = haversine_distance(user["location"], provider["location"])
        if distance > 10:  # Skip if out of range
            continue
        

        # Get image preview URLs
        img_urls = []
        if req.get("attachment_id"):
            img_urls.append(f"/provider/attachment/{str(req['attachment_id'])}")

        formatted = format_request_for_provider(req, user, distance, img_urls)
        results.append(formatted)

    return results


def update_duty_status(provider_id, status):
   
    if status not in ["on", "off"]:
        return {"msg": "Invalid duty status"}, 400

    mongo.db.providers.update_one({"_id": ObjectId(provider_id)}, {"$set": {"duty_status": status}})
    return {"msg": f"Duty status set to {status}"}


def accept_or_reject_request(provider_id, request_id, action):
    

    if action not in ["accept", "reject"]:
        return {"msg": "Invalid action"}, 400

    req = mongo.db.requests.find_one({"_id": ObjectId(request_id)})

    if not req:
        return {"msg": "Request not found"}, 404

    # Update status
    mongo.db.requests.update_one(
        {"_id": ObjectId(request_id)},
        {"$set": {
            "status": action.capitalize(),
            "handled_by": ObjectId(provider_id)
        }}
    )

    return {"msg": f"Request {action}ed successfully"}
