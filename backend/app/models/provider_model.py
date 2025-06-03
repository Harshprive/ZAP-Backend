from app.extensions import mongo
from bson import ObjectId

# Insert initial provider data (step 1: basic info)
def insert_provider(data):
    return mongo.db.providers.insert_one(data)

# Update document verification (step 2)
def update_document_verification(provider_id, documents):
    return mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"documents": documents, "document_verified": True}}
    )

# Update professional details (step 3)
def update_professional_details(provider_id, professional):
    return mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"professional_details": professional}}
    )

# Update service selection (step 4)
def update_service_selection(provider_id, services):
    return mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"services": services}}
    )

# Update appointment setup (step 5)
def update_appointment_details(provider_id, appointment):
    return mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {"$set": {"appointment": appointment}}
    )

def get_available_providers_by_service(service):
    return list(mongo.db.providers.find({"services.main": service, "available": True}))

def get_provider_by_id(provider_id):
    return mongo.db.providers.find_one({"_id": ObjectId(provider_id)})

def get_provider_by_email(email):
    return mongo.db.providers.find_one({"email": email})



from bson import ObjectId

# ✅ Get provider by ID
def get_provider_by_id(provider_id):
    return mongo.db.providers.find_one({"_id": ObjectId(provider_id)})

# ✅ Update provider location
def update_provider_location(provider_id, lat, lon):
    result = mongo.db.providers.update_one(
        {"_id": ObjectId(provider_id)},
        {
            "$set": {
                "location": {
                    "latitude": lat,
                    "longitude": lon
                }
            }
        }
    )
    return result.modified_count > 0

# ✅ Get all providers with specific service
def get_providers_by_service(service):
    return list(mongo.db.providers.find({
        "services.main_service": service
    }))


def format_request_for_provider(request_doc, user_doc, distance_km, eta_min, image_urls):
    return {
        "request_id": str(request_doc["_id"]),
        "service": request_doc["subcategory"],
        "description": request_doc["issue"],
        "user_name": user_doc.get("name", "N/A"),
        "location": user_doc.get("location", {}),
        "distance_km": round(distance_km, 2),
        "estimated_time_min": eta_min,
        "attachments": image_urls,
        "status": request_doc.get("status", "Pending")
    }

