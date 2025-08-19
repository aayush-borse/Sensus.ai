import requests
from config import LT_BASE

LT_URL = LT_BASE.rstrip('/') + '/translate'

def translate(text: str, source: str, target: str):
    payload = {"q": text, "source": source, "target": target, "format": "text"}
    try:
        r = requests.post(LT_URL, data=payload, timeout=8)
        r.raise_for_status()
        data = r.json()
        return data.get("translatedText") or data.get("translated") or ""
    except Exception:
        return text
