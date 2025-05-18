from app.extensions import mongo
from bson import ObjectId

def insert_user(data):
    return mongo.db.users.insert_one(data)

def get_user_by_email(email):
    return mongo.db.users.find_one({"email": email})

def get_user_by_id(user_id):
    return mongo.db.users.find_one({"_id": ObjectId(user_id)})
