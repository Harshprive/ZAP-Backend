from app.extensions import mongo
from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/my_mvp_app")
db = client["zap_services"]
match_collection = db["matches"]
def insert_location(user_id, lat, lng, role):
    return mongo.db.locations.insert_one({
        "user_id": user_id,
        "lat": lat,
        "lng": lng,
        "role": role  # "user" or "provider"
    })

def get_location_by_user(user_id):
    return mongo.db.locations.find_one({"user_id": user_id})

def create_match(match_data):
    return match_collection.insert_one(match_data)

def get_matches_by_user(user_id):
    return list(match_collection.find({"user_id": user_id}))