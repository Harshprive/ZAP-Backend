from math import radians, cos, sin, asin, sqrt

def haversine_distance(loc1, loc2):
    lon1, lat1, lon2, lat2 = map(radians, [
        loc1["longitude"], loc1["latitude"],
        loc2["longitude"], loc2["latitude"]
    ])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    return 6371 * c
