# app/models/service_model.py

from app.extensions import mongo
from pymongo import MongoClient
client = MongoClient("mongodb://localhost:27017/")
db = client["zap_services"]
services_collection = db["services"]
def get_all_services():
    return list(mongo.db.services.find())

def search_services(query):
    return list(mongo.db.services.find({
        "name": {"$regex": query, "$options": "i"}
    }))

def get_top_recommended_services():
    return list(mongo.db.services.find().sort("booking_count", -1).limit(5))

def add_service_from_provider(service_data):
    existing = services_collection.find_one({
        "category": service_data["category"],
        "subcategory": service_data["subcategory"]
    })
    if not existing:
        services_collection.insert_one(service_data)