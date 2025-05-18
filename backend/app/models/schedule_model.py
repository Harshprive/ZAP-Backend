# app/models/schedule_model.py

from app.extensions import mongo
from datetime import datetime

def schedule_service(user_id, service_name):
    schedule_doc = {
        "user_id": user_id,
        "service": service_name,
        "scheduled_at": datetime.utcnow(),
        "status": "waiting"
    }
    mongo.db.schedules.insert_one(schedule_doc)
    return True
