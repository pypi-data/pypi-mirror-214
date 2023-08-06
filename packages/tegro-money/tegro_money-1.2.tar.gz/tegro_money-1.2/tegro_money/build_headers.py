import json
import hmac
import hashlib
from typing import Dict


def build_headers(api_key: str, data: Dict) -> Dict:
    body = json.dumps(data)
    sign = hmac.new(
        body.encode('utf-8'), 
        api_key.encode('utf-8'), 
        hashlib.sha256
        ).hexdigest()
    headers ={
    "Authorization": f"Bearer {sign}",
    "Content-Type": "application/json"
    }
    return headers