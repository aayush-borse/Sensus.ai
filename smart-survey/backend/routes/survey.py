from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.db import db
from core.fraud import hard_reject_rules, soft_flag_checks, score_vector
from datetime import datetime, timedelta

bp = Blueprint('survey', __name__, url_prefix='/api/v1/survey')
SURVEYS = db.surveys
RESPONSES = db.responses

@bp.route('/questions', methods=['GET'])
@jwt_required()
def get_questions():
    surveyId = request.args.get('surveyId')
    lang = request.args.get('lang', 'en')
    if not surveyId:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": "surveyId required"}}), 400
    sv = SURVEYS.find_one({"_id": surveyId})
    if not sv:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Survey not found"}}), 404
    questions = []
    for q in sv.get('questions', []):
        prompt = q.get('prompt', {})
        text = prompt.get(lang) or prompt.get('en') or ''
        questions.append({"id": q['id'], "type": q['type'], "prompt": text, "required": q.get('required', False), **({"options": q.get('options')} if q.get('options') else {})})
    return jsonify({"surveyId": surveyId, "language": lang, "questions": questions}), 200

@bp.route('/submit', methods=['POST'])
@jwt_required()
def submit():
    payload = request.get_json() or {}
    surveyId = payload.get('surveyId')
    deviceId = payload.get('deviceId')
    language = payload.get('language', 'en')
    answers = payload.get('answers', [])
    location = payload.get('location')
    completion_time = payload.get('completionTimeSeconds')

    if not surveyId or not deviceId or not answers:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": "Missing fields"}}), 400
    sv = SURVEYS.find_one({"_id": surveyId})
    if not sv:
        return jsonify({"error": {"code": "NOT_FOUND", "message": "Survey not found"}}), 404

    rules = hard_reject_rules(answers, sv.get('questions', []), payload)
    if rules:
        return jsonify({"status": "rejected", "reason": "; ".join([r['rule'] for r in rules]), "error": {"code": "HARD_REJECT", "message": "Hard reject rules triggered", "details": rules}}), 422

    ten_minutes_ago = datetime.utcnow() - timedelta(minutes=10)
    recent = RESPONSES.find({"surveyId": surveyId, "deviceId": deviceId, "createdAt": {"$gte": ten_minutes_ago}}).sort('createdAt', -1).limit(5)
    recent = list(recent)
    recent_duplicates = False
    for r in recent:
        match_count = 0
        for a in answers:
            for ra in r.get('answers', []):
                if a['questionId'] == ra['questionId'] and str(a.get('value')) == str(ra.get('value')):
                    match_count += 1
        if match_count / max(1, len(answers)) > 0.8:
            recent_duplicates = True
            break

    numeric_vec = []
    for q in sv.get('questions', []):
        if q.get('type') == 'number':
            found = next((a for a in answers if a['questionId'] == q['id']), None)
            try:
                numeric_vec.append(float(found['value']) if found else 0.0)
            except Exception:
                numeric_vec.append(0.0)
    anomaly_score = score_vector(numeric_vec)

    soft_flags = soft_flag_checks(answers, sv.get('questions', []), payload, completion_time, recent_duplicates)
    suspect = bool(soft_flags or anomaly_score > 0.8)

    resp_doc = {
        "surveyId": surveyId,
        "userId": get_jwt_identity(),
        "deviceId": deviceId,
        "language": language,
        "answers": answers,
        "location": location,
        "fraud": {"hardRejected": False, "rules": [], "anomalyScore": float(anomaly_score), "suspect": suspect, "softFlags": soft_flags},
        "createdAt": datetime.utcnow()
    }

    res = RESPONSES.insert_one(resp_doc)
    return jsonify({"responseId": str(res.inserted_id), "status": "accepted", "fraud": resp_doc['fraud']}), 201
