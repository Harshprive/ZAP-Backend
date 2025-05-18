from app.extensions import mongo
from app.utils.location_utils import haversine_distance
from app.models.user_model import get_user_by_id
from app.models.provider_model import get_available_providers_by_service
from app.models.request_model import insert_request
from app.models.log_model import insert_log
from datetime import datetime
from bson import ObjectId

def match_user_with_providers(user_id, service):
    user = get_user_by_id(user_id)
    if not user:
        return {"msg": "User not found"}, 404

    user_loc = user["location"]
    providers = get_available_providers_by_service(service)

    hotspot_providers = []
    for p in providers:
        dist = haversine_distance(user_loc, p["location"])
        if dist <= 10:
            p["distance"] = round(dist, 2)
            hotspot_providers.append(p)

    if not hotspot_providers:
        mongo.db.schedule_queue.insert_one({
            "user_id": ObjectId(user_id),
            "service": service,
            "timestamp": datetime.utcnow()
        })
        insert_log({
            "action": "Request Scheduled",
            "user_id": ObjectId(user_id),
            "service": service,
            "timestamp": datetime.utcnow()
        })
        return {"msg": "No providers available, request added to schedule"}, 200

    selected = hotspot_providers[0]
    est_time = int((selected["distance"] / 30) * 60)

    insert_request({
        "user_id": ObjectId(user_id),
        "provider_id": selected["_id"],
        "service": service,
        "distance_km": selected["distance"],
        "estimated_time_min": est_time,
        "status": "matched",
        "timestamp": datetime.utcnow()
    })

    insert_log({
        "action": "Request Matched",
        "user_id": ObjectId(user_id),
        "provider_id": selected["_id"],
        "service": service,
        "timestamp": datetime.utcnow()
    })

    return {
        "msg": "Provider matched",
        "provider": {
            "name": selected["name"],
            "distance_km": selected["distance"],
            "estimated_time_min": est_time
        }
    }, 200
