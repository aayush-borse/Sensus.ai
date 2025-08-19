from core.db import db
from datetime import datetime
SURVEYS = db.surveys
USERS = db.users

if not USERS.find_one({"email": "admin@neksha.ai"}):
    USERS.insert_one({"name": "Admin", "email": "admin@neksha.ai", "passwordHash": "$2b$12$Df63AfnacDwjf4bayuvvfeY0d5h6qQV.qD5QtSPulDGM1er4CtH3u", "role": "admin", "createdAt": datetime.utcnow()})

survey = {
    "_id": "svy_123",
    "title": "Demographic survey",
    "languages": ["en", "hi"],
    "active": True,
    "createdAt": datetime.utcnow(),
    "questions": [
        {"id": "q1", "type": "text", "prompt": {"en": "What is your name?", "hi": "आपका नाम?"}, "required": True},
        {"id": "q2", "type": "number", "prompt": {"en": "Age?", "hi": "आयु?"}, "min": 0, "max": 120, "required": True},
        {"id": "q3", "type": "choice", "prompt": {"en": "Gender?", "hi": "लिंग?"}, "options": ["Male", "Female", "Other"], "required": True}
    ]
}

if not SURVEYS.find_one({"_id": "svy_123"}):
    SURVEYS.insert_one(survey)
    print("Inserted demo survey svy_123")
else:
    print("Demo survey exists")
