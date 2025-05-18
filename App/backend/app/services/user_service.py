# app/services/user_service.py

from flask import jsonify
from werkzeug.security import check_password_hash
from app.extensions import mongo, jwt
from flask_jwt_extended import create_access_token
from bson.objectid import ObjectId

def register_user(data):
    users = mongo.db.users
    if users.find_one({"email": data["email"]}):
        return {"msg": "User already exists"}, 400

    user = {
        "username": data["username"],
        "email": data["email"],
        "password": data["password"],  # Ideally hash it!
        "role": data.get("role", "user"),
        "location": data.get("location"),
        "service_required": data.get("service_required", None)
    }
    users.insert_one(user)
    return {"msg": "User registered successfully"}, 201

def login_user(data):
    users = mongo.db.users
    user = users.find_one({"email": data["email"]})

    if not user or user["password"] != data["password"]:
        return {"msg": "Invalid email or password"}, 401

    access_token = create_access_token(identity=str(user["_id"]))
    return {"token": access_token}, 200
