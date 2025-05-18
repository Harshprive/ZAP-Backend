from geopy.distance import geodesic

# app/services/location_service.py

from app.extensions import mongo

def add_location(data):
    entity_id = data.get("entity_id")
    latitude = data.get("latitude")
    longitude = data.get("longitude")
    entity_type = data.get("type")  # 'user' or 'provider'

    if not all([entity_id, latitude, longitude, entity_type]):
        return {"error": "Missing data"}, 400

    mongo.db.locations.insert_one({
        "entity_id": entity_id,
        "latitude": latitude,
        "longitude": longitude,
        "type": entity_type
    })

    return {"message": "Location added successfully"}, 201

def get_distance_km(coord1, coord2):
    """
    Given two sets of coordinates (latitude, longitude), calculate the distance in kilometers.
    coord1 and coord2 should be tuples: (latitude, longitude)
    """
    return geodesic(coord1, coord2).km