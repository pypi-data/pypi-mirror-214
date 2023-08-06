import requests
import json
from typing import Dict
from .build_dict import build_dict
from .build_headers import build_headers


def post(shop_id: str, api_key: str, api_url: str, endpoint: str, body: Dict = None) -> Dict:
    url = api_url + endpoint
    body = build_dict(shop_id, body)
    headers = build_headers(api_key, body)
    try:
        response = requests.post(url, data=body, headers=headers)
        response.raise_for_status()
        response_text = json.loads(response.text)
        return response_text
    except Exception as e:
        print(e)
        return None