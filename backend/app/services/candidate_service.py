from datetime import datetime

from app.database.mongodb import database


candidates_collection = database["candidates"]


def create_candidate(resume_data: dict):
    now = datetime.utcnow()

    candidate = {
        "name": None,
        "email": None,
        "phone": None,
        "location": None,
        "summary": None,

        "skills": [],
        "experience": [],
        "education": [],
        "certifications": [],

        "resume": resume_data,

        "processing": {
            "status": "uploaded",
            "model": None,
            "processed_at": None
        },

        "created_at": now,
        "updated_at": now
    }

    result = candidates_collection.insert_one(candidate)

    return result.inserted_id