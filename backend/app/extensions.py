from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager
from gridfs import GridFS
mongo = PyMongo()
jwt = JWTManager()

def init_fs(app):
    global fs
    mongo.init_app(app)
    fs = GridFS(mongo.db)