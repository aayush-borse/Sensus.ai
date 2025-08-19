from flask import Blueprint, request, jsonify
from core.translate import translate

bp = Blueprint('utils', __name__, url_prefix='/api/v1/utils')

@bp.route('/translate', methods=['POST'])
def proxy_translate():
    data = request.get_json() or {}
    text = data.get('text')
    source = data.get('source', 'en')
    target = data.get('target', 'hi')
    if not text:
        return jsonify({"error": {"code": "VALIDATION_ERROR", "message": "text is required"}}), 400
    translated = translate(text, source, target)
    return jsonify({"translated": translated}), 200
