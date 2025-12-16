import uuid
from datetime import datetime
from decimal import Decimal


def uid():
    return str(uuid.uuid4())

def now_ts():
    return datetime.utcnow()

def safe_div(a, b):
    return a / b if b else 0.0

def normalize(val, minv=0.0, maxv=1.0):
    if val is None:
        return 0.0
    if val <= minv: 
        return 0.0
    if val >= maxv:
        return 1.0
    return (val - minv) / (maxv - minv)

def to_json_safe(value):
    if isinstance(value, Decimal):
        return float(value)
    if isinstance(value, dict):
        return {k: to_json_safe(v) for k, v in value.items()}
    if isinstance(value, list):
        return [to_json_safe(v) for v in value]
    return value

