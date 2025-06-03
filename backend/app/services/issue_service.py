from bson import ObjectId
from app.extensions import mongo , fs
from app.models.issue_model import create_issue_model



def submit_issue(user_id, json_data, file):
    attachment_id = None

    if file:
        attachment_id = fs.put(file, filename=file.filename, content_type=file.content_type)

    issue_data = {
        "user_id": str(user_id),
        "issue": json_data.get("issue"),
        "min_days": int(json_data.get("min_days", 1)),
        "attachment_type": "image"  # or pdf etc.
    }

    issue_doc = create_issue_model(issue_data, attachment_id)
    result = mongo.db.issues.insert_one(issue_doc)

    return {"msg": "Issue submitted", "issue_id": str(result.inserted_id)}
