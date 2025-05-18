from app.extensions import mongo

def insert_log(log_data):
    return mongo.db.admin_logs.insert_one(log_data)

def get_all_logs():
    return list(mongo.db.admin_logs.find())
