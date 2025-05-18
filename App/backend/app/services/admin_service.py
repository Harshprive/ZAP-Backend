from app.models.log_model import get_all_logs

def fetch_logs():
    logs = get_all_logs()
    for log in logs:
        log["_id"] = str(log["_id"])
    return logs
# active provider
# provider = no. of sercices /no of bookings/ no of scheduls/ no, of issues /no. of reques per week day month for all /reason of canclation
# active user / no. of booking / no , of schedul / no. of issues /reason of canclation
# no.of cancelation by both 
