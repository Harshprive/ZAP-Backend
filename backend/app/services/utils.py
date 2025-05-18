# app/services/utils.py

from geopy.distance import geodesic

# app/services/utils.py

def get_distance_km(coord1, coord2):
    # Calculate the distance between two coordinates (latitude, longitude)
    from math import radians, sin, cos, sqrt, atan2

    # convert latitude and longitude from degrees to radians
    lat1, lon1 = coord1
    lat2, lon2 = coord2

    # haversine formula
    R = 6371  # Radius of Earth in km
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    
    distance = R * c  # Result in kilometers
    return distance
