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
