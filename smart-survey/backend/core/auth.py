from core.db import db
import bcrypt
from flask_jwt_extended import create_access_token

USERS = db.users

def hash_password(plain: str) -> str:
    return bcrypt.hashpw(plain.encode(), bcrypt.gensalt()).decode()

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode(), hashed.encode())
    except Exception:
        return False

def create_user(name, email, password, role="collector"):
    if USERS.find_one({"email": email}):
        return None
    pwd = hash_password(password)
    doc = {"name": name, "email": email, "passwordHash": pwd, "role": role}
    res = USERS.insert_one(doc)
    doc["_id"] = str(res.inserted_id)
    return doc

def authenticate(email, password):
    user = USERS.find_one({"email": email})
    if not user:
        return None
    if not verify_password(password, user["passwordHash"]):
        return None
    token = create_access_token(identity=str(user["_id"]))
    return {"userId": str(user["_id"]), "token": token}
