from flask import Flask, jsonify
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import config

# Simple in-memory rate limiter (per-IP, windowed)
from time import time
_rate_store = {}

def simple_rate_limiter(key, window=60, max_calls=30):
    now = int(time())
    calls = _rate_store.get(key, [])
    # remove old
    calls = [t for t in calls if t > now - window]
    if len(calls) >= max_calls:
        return False
    calls.append(now)
    _rate_store[key] = calls
    return True

from routes.auth import bp as auth_bp
from routes.survey import bp as survey_bp
from routes.admin import bp as admin_bp
from routes.utils import bp as utils_bp

app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = config.JWT_SECRET
jwt = JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": config.CORS_ORIGINS}})

app.register_blueprint(auth_bp)
app.register_blueprint(survey_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(utils_bp)

@app.errorhandler(422)
def handle_422(err):
    return jsonify({"error": {"code": "VALIDATION_ERROR", "message": str(err)}}), 422

@app.errorhandler(500)
def handle_500(err):
    return jsonify({"error": {"code": "SERVER_ERROR", "message": "Internal server error"}}), 500

if __name__ == '__main__':
    # Listen on all interfaces for Docker
    app.run(host="0.0.0.0", port=5000, debug=True)
