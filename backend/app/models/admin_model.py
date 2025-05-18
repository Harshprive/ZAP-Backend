from app.extensions import mongo

def get_admin_by_email(email):
    return mongo.db.admins.find_one({"email": email})

def insert_admin(admin_data):
    return mongo.db.admins.insert_one(admin_data)
