# config.py
import os

# MongoDB connection (default to local if env not set)
MONGO_URI = os.getenv("MONGO_URI", "mongodb://mongo:27017/smart_survey")

# JWT secret key (default for testing)
JWT_SECRET = os.getenv("JWT_SECRET", "supersecretjwtkey")

# LibreTranslate base URL (default)
LT_BASE = os.getenv("LT_BASE", "https://libretranslate.com")

# CORS origins (default to allow all)
CORS_ORIGINS = os.getenv("CORS_ORIGINS", "*")

# Rate limiting defaults
RATE_LIMIT_WINDOW = int(os.getenv("RATE_LIMIT_WINDOW", "60"))
RATE_LIMIT_MAX = int(os.getenv("RATE_LIMIT_MAX", "30"))
