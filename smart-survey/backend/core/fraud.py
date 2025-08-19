from sklearn.ensemble import IsolationForest
import numpy as np
from datetime import datetime, timedelta

model = None

def fit_isolationforest(numeric_vectors):
    global model
    if len(numeric_vectors) < 10:
        return None
    X = np.array(numeric_vectors)
    model = IsolationForest(contamination=0.05, random_state=42)
    model.fit(X)
    return model

def score_vector(vec):
    global model
    if model is None:
        return 0.5
    try:
        score = -model.decision_function([vec])[0]
        s = 1 / (1 + np.exp(-score))
        return float(s)
    except Exception:
        return 0.5

def hard_reject_rules(answers, questions, payload):
    rules = []
    qmap = {q['id']: q for q in questions}
    for a in answers:
        qid = a['questionId']
        if qid not in qmap:
            continue
        q = qmap[qid]
        if q.get('type') == 'number':
            try:
                val = float(a['value'])
            except Exception:
                rules.append({'rule': 'invalid_number', 'questionId': qid})
                continue
            minv = q.get('min', None)
            maxv = q.get('max', None)
            if minv is not None and val < minv:
                rules.append({'rule': 'below_min', 'questionId': qid})
            if maxv is not None and val > maxv:
                rules.append({'rule': 'above_max', 'questionId': qid})
    if not payload.get('location'):
        rules.append({'rule': 'gps_missing'})
    for q in questions:
        if q.get('required'):
            found = any(a['questionId'] == q['id'] and a.get('value') not in [None, ""] for a in answers)
            if not found:
                rules.append({'rule': 'required_unanswered', 'questionId': q['id']})
    return rules

def soft_flag_checks(answers, questions, payload, completion_time_seconds, recent_duplicates=False):
    flags = []
    qcount = max(1, len(questions))
    if completion_time_seconds is not None and completion_time_seconds / qcount < 3:
        flags.append('fast_completion')
    if payload.get('location') and payload['location'].get('accuracy', 0) > 100:
        flags.append('low_gps_accuracy')
    if recent_duplicates:
        flags.append('recent_duplicate')
    return flags
