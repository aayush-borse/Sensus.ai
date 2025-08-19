# Smart Survey MVP (backend + frontend skeleton)

This archive contains a runnable Flask backend and an Expo React Native frontend skeleton.

## Quick start

### Backend
1. Create venv:
   ```
   python -m venv .venv
   source .venv/bin/activate
   pip install -r backend/requirements.txt
   ```
2. Start MongoDB (local or Atlas).
3. Copy `.env.example` to `.env` and update values.
4. Seed demo data:
   ```
   python backend/seed.py
   ```
5. Run backend:
   ```
   export FLASK_ENV=development
   export MONGO_URI="mongodb://localhost:27017/smart_survey"
   export JWT_SECRET="devsecret"
   export LT_BASE="https://libretranslate.com"
   flask --app backend.app run -p 5000
   ```

### Frontend
1. Install:
   ```
   cd frontend
   npm install
   npx expo start
   ```
2. Open on Expo Go or emulator.

## Notes
- Admin user created by seed uses a placeholder bcrypt hash; replace before production.
- The IsolationForest trainer is a stub — for production persist model and run periodic training.
- Replace CORS origins and secrets in `.env` before deployment.



Admin credentials (seed): admin@neksha.ai / adminpass

Final archive name: Neksha Ai.zip
