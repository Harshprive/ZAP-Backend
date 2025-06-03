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

    user_location = user.get("location")
    if not user_location:
        return {"msg": "User location not found"}, 400

    providers = get_available_providers_by_service(service)
    matched_providers = []

    for provider in providers:
        provider_loc = provider.get("location")
        if not provider_loc:
            continue

        dist = haversine_distance(user_location, provider_loc)
        if dist <= 10:
            provider["distance"] = round(dist, 2)
            matched_providers.append(provider)

    if not matched_providers:
        mongo.db.schedule_queue.insert_one({
            "user_id": ObjectId(user_id),
            "service": service,
            "timestamp": datetime.utcnow()
        })
        insert_log({
            "action": "Scheduled Request",
            "user_id": ObjectId(user_id),
            "service": service,
            "timestamp": datetime.utcnow()
        })
        return {"msg": "No provider found nearby, request added to schedule"}, 200

    # Select nearest
    matched_providers.sort(key=lambda x: x["distance"])
    selected = matched_providers[0]
    est_time = int((selected["distance"] / 30) * 60)  # 30 km/h speed

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
        "action": "Matched",
        "user_id": ObjectId(user_id),
        "provider_id": selected["_id"],
        "service": service,
        "timestamp": datetime.utcnow()
    })

    return {
        "msg": "Provider matched",
        "provider": {
            "name": selected.get("name"),
            "distance_km": selected["distance"],
            "estimated_time_min": est_time
        }
    }, 200
