from flask import Blueprint, request, jsonify
from core.db import db
from core.auth import create_user, verify_password
from flask_jwt_extended import create_access_token

bp = Blueprint('auth', __name__, url_prefix='/api/v1/auth')

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json() or {}
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')
    if not name or not email or not password:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": "Missing fields"}}), 400
    if db.users.find_one({"email": email}):
        return jsonify({"error": {"code": "EMAIL_EXISTS", "message": "Email already exists"}}), 409
    user = create_user(name, email, password)
    token = create_access_token(identity=str(user['_id']))
    return jsonify({"userId": user['_id'], "token": token}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')
    if not email or not password:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": "Missing fields"}}), 400
    user = db.users.find_one({"email": email})
    if not user:
        return jsonify({"error": {"code": "INVALID_CREDENTIALS", "message": "Unauthorized"}}), 401
    if not verify_password(password, user['passwordHash']):
        return jsonify({"error": {"code": "INVALID_CREDENTIALS", "message": "Unauthorized"}}), 401
    token = create_access_token(identity=str(user['_id']))
    return jsonify({"userId": str(user['_id']), "token": token}), 200
