import json

def parse_json_safe(raw_output):
    """Handle both string and dict outputs from chains"""
    print(f"parse_json_safe input type: {type(raw_output)}")
    
    # If already a dict (from JsonOutputParser), return directly
    if isinstance(raw_output, dict):
        return raw_output, None
    
    # If string, try JSON parsing
    if isinstance(raw_output, str) and raw_output.strip():
        try:
            return json.loads(raw_output), None
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}")
            return {}, f"JSON parse failed: {e}"
    
    # Empty or None
    return {}, "No output received"

import json
from typing import Tuple, Any

def parse_and_filter(raw_output, schema) -> Tuple[Any, str]:
       # Step 1: Safe parse
    parsed, parse_err = parse_json_safe(raw_output)
    if parse_err:
        return {}, f"Parse error: {parse_err}"

    # Step 2: Determine allowed keys
    allowed_keys = []
    if "required" in schema:
        allowed_keys = schema["required"]
    elif "properties" in schema:
        allowed_keys = list(schema["properties"].keys())

    # Step 3: Filter dict(s) recursively
    def filter_dict(obj):
        if isinstance(obj, dict):
            return {k: filter_dict(v) for k, v in obj.items() if k in allowed_keys}
        elif isinstance(obj, list):
            return [filter_dict(item) for item in obj]
        else:
            return obj

    filtered = filter_dict(parsed)
    return filtered, None



RCA_SCHEMA = {"type": "object", "required": ["root_causes"]}
BRIEF_SCHEMA = {"type": "object", "required": ["title", "summary"]}
ACTIONS_SCHEMA = {"type": "array"}
EMAIL_SCHEMA = {"type": "object", "required": ["subject", "body_text"]}
