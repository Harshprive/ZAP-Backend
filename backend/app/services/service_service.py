

from app.models.service_model import *

def fetch_all_services():
    services = get_all_services()
    for s in services:
        s["_id"] = str(s["_id"])
    return services

def search_for_services(query):
    results = search_services(query)
    for s in results:
        s["_id"] = str(s["_id"])
    return results

def get_recommended_services():
    top = get_top_recommended_services()
    for s in top:
        s["_id"] = str(s["_id"])
    return top
