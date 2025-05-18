from app.extensions import mongo

def insert_request(request_data):
    return mongo.db.requests.insert_one(request_data)
