from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, timedelta
from app.extensions import mongo , fs
import jwt as jwt_lib
from bson import ObjectId
from app.models.provider_model import get_provider_by_email
from gridfs import GridFS
JWT_SECRET_KEY = "6HPFW3INuRkpko4jGQkp9K98ecvokCZuBRlNi5kxfOI"
  # Replace with env variable in production

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
        "created_at": datetime.utcnow()
    }

    providers.insert_one(provider)
    return {"msg": "Provider registered successfully"}, 201

# Step 2: Login
def login_provider(data):
    provider = get_provider_by_email(data["email"])

    if not provider or not check_password_hash(provider["password"], data["password"]):
        return {"msg": "Invalid email or password"}, 401

    payload = {
        "sub": str(provider["_id"]),
        "email": provider["email"],
        "role": "provider",
        "iat": datetime.utcnow(),
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt_lib.encode(payload, JWT_SECRET_KEY, algorithm="HS256")

    return {"msg": "Login successful", "token": token}, 200
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
    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"services": data}}
    )
    return {"msg": "Services added successfully"}, 200

# Step 6: Set appointment
def set_appointment(provider_id, data):
    mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"appointment": data, "available": True}}
    )
    return {"msg": "Appointment setup complete"}, 200
