from app.extensions import mongo

def insert_location(user_id, lat, lng, role):
    return mongo.db.locations.insert_one({
        "user_id": user_id,
        "lat": lat,
        "lng": lng,
        "role": role  # "user" or "provider"
    })

def get_location_by_user(user_id):
    return mongo.db.locations.find_one({"user_id": user_id})
