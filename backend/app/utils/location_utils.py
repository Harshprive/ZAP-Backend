from math import radians, cos, sin, sqrt, atan2

import math

def haversine_distance(loc1, loc2):
    """
    loc1 and loc2 are dicts with 'latitude' and 'longitude'
    Returns distance in kilometers.
    """
    R = 6371  # Earth radius in km
    lat1 = math.radians(loc1["latitude"])
    lon1 = math.radians(loc1["longitude"])
    lat2 = math.radians(loc2["latitude"])
    lon2 = math.radians(loc2["longitude"])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    return R * c