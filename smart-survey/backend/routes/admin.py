from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from core.db import db
from core.analytics import summary_for_survey, bar_for_question, timeline_for_survey, heatmap_bins

bp = Blueprint('admin', __name__, url_prefix='/api/v1/admin')

def require_admin():
    uid = get_jwt_identity()
    u = db.users.find_one({"_id": uid})
    if not u or u.get('role') != 'admin':
        return False
    return True

@bp.route('/analytics/summary', methods=['GET'])
@jwt_required()
def summary():
    if not require_admin():
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Admin only"}}), 403
    surveyId = request.args.get('surveyId')
    return jsonify(summary_for_survey(surveyId)), 200

@bp.route('/visuals/bar', methods=['GET'])
@jwt_required()
def bar():
    if not require_admin():
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Admin only"}}), 403
    surveyId = request.args.get('surveyId')
    questionId = request.args.get('questionId')
    return jsonify(bar_for_question(surveyId, questionId)), 200

@bp.route('/visuals/pie', methods=['GET'])
@jwt_required()
def pie():
    if not require_admin():
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Admin only"}}), 403
    surveyId = request.args.get('surveyId')
    questionId = request.args.get('questionId')
    res = bar_for_question(surveyId, questionId)
    total = sum(res['values']) if res['values'] else 0
    if total == 0:
        return jsonify({"labels": res['labels'], "values": []})
    values = [v / total for v in res['values']]
    return jsonify({"labels": res['labels'], "values": values}), 200

@bp.route('/visuals/heatmap', methods=['GET'])
@jwt_required()
def heatmap():
    if not require_admin():
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Admin only"}}), 403
    surveyId = request.args.get('surveyId')
    x = request.args.get('x')
    y = request.args.get('y')
    return jsonify(heatmap_bins(surveyId, x, y)), 200

@bp.route('/visuals/timeline', methods=['GET'])
@jwt_required()
def timeline():
    if not require_admin():
        return jsonify({"error": {"code": "UNAUTHORIZED", "message": "Admin only"}}), 403
    surveyId = request.args.get('surveyId')
    interval = request.args.get('interval', 'day')
    return jsonify(timeline_for_survey(surveyId, interval)), 200
