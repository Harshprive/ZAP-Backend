from datetime import datetime

def create_issue_model(data, attachment_id=None):
    return {
        "user_id": data["user_id"],
        "issue": data["issue"],
        "attachment_type": data.get("attachment_type", "image"),
        "attachment_id": attachment_id,
        "min_days_to_solve": data["min_days"],
        "submitted_at": datetime.utcnow(),
        "status": "Pending"
    }
