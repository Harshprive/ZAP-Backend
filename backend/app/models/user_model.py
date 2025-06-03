# app/models/user_model.py
from bson import ObjectId
from app.extensions import mongo

def create_user(data):
    return mongo.db.users.insert_one(data)

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})

def update_user_location(user_id, location_data):
    return mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"location": location_data}}
    )

def save_user_preferred_services(user_id, services):
    return mongo.db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": {"preferred_services": services}}
    )

