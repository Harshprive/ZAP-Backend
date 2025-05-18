from app.extensions import mongo


def add_to_schedule(user_id, service_name):
    mongo.db.scheduled.insert_one({
        "user_id": user_id,
        "service": service_name,
        "status": "waiting"
    })
