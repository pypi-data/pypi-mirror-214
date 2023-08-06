import time
from typing import Dict


def build_dict(shop_id: str, data: Dict = None) -> Dict:
    nonce = str(int(time.time()))
    default_dict = {
        "shop_id": shop_id,
        "nonce": nonce
    }
    if not data:
        return default_dict
    else:
        result = {**default_dict, **data}
        return result