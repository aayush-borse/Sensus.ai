from core.db import db
RESP = db.responses
from datetime import datetime, timedelta

def summary_for_survey(surveyId):
    pipeline = [
        {"$match": {"surveyId": surveyId}},
        {"$group": {"_id": None, "count": {"$sum": 1}, "suspect": {"$sum": {"$cond": ["$fraud.suspect", 1, 0]}}}},
    ]
    res = list(RESP.aggregate(pipeline))
    if res:
        return {"total": res[0]['count'], "suspect": res[0]['suspect']}
    return {"total": 0, "suspect": 0}

def bar_for_question(surveyId, questionId):
    pipeline = [
        {"$match": {"surveyId": surveyId}},
        {"$unwind": "$answers"},
        {"$match": {"answers.questionId": questionId}},
        {"$group": {"_id": "$answers.value", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}}
    ]
    rows = list(RESP.aggregate(pipeline))
    labels = [r['_id'] for r in rows]
    values = [r['count'] for r in rows]
    return {"labels": labels, "values": values}

def timeline_for_survey(surveyId, interval='day'):
    if interval != 'day':
        interval = 'day'
    pipeline = [
        {"$match": {"surveyId": surveyId}},
        {"$group": {"_id": {"$dateToString": {"format": "%Y-%m-%d", "date": "$createdAt"}}, "count": {"$sum": 1}}},
        {"$sort": {"_id": 1}}
    ]
    rows = list(RESP.aggregate(pipeline))
    timestamps = [r['_id'] for r in rows]
    counts = [r['count'] for r in rows]
    return {"timestamps": timestamps, "counts": counts}

def heatmap_bins(surveyId, x_q, y_q, x_bins=5, y_bins=5):
    docs = RESP.find({"surveyId": surveyId})
    xs, ys = [], []
    for d in docs:
        for a in d.get('answers', []):
            if a['questionId'] == x_q:
                try:
                    xs.append(float(a['value']))
                except Exception:
                    pass
            if a['questionId'] == y_q:
                try:
                    ys.append(float(a['value']))
                except Exception:
                    pass
    import numpy as np
    if not xs or not ys:
        return {"xBins": [], "yBins": [], "matrix": []}
    x_edges = np.linspace(min(xs), max(xs), x_bins + 1).tolist()
    y_edges = np.linspace(min(ys), max(ys), y_bins + 1).tolist()
    matrix = [[0 for _ in range(y_bins)] for _ in range(x_bins)]
    for i in range(len(xs)):
        xi = min(int((xs[i] - x_edges[0]) / (x_edges[-1] - x_edges[0]) * x_bins), x_bins - 1)
        yi = min(int((ys[i] - y_edges[0]) / (y_edges[-1] - y_edges[0]) * y_bins), y_bins - 1)
        matrix[xi][yi] += 1
    return {"xBins": x_edges, "yBins": y_edges, "matrix": matrix}
