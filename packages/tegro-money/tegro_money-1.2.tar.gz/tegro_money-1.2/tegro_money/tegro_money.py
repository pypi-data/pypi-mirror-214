from .api import post
from typing import List, Dict
from .build_dict import build_dict
from .tegro_config import TegroConfig

class TegroMoneyParser:
    def __init__(self, config: TegroConfig, endpoints: Dict = None):
        """
        :param config: TegroConfig
        :param enpoints: endpoints in dict format (as default_endpoints)
        """

        default_endpoints = {
                "create_order": "createOrder",
                "shops_list": "shops",
                "balance": "balance",
                "order_info": "order",
                "orders_list": "orders",
                "create_withdrawal": "createWithdrawal",
                "withdrawals_list": "withdrawals",
                "withdrawal_info": "withdrawal"
            }

        self.config = config.dict()
        self.endpoints = endpoints or default_endpoints

    def shops_list(self) -> List[Dict]:
        body = build_dict(self.config["shop_id"])
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["shops_list"], 
            body
            )
        if result:
            shops = result["data"]["shops"]
            return shops
        else:
            return None
        
    def balance(self) -> Dict:
        body = build_dict(self.config["shop_id"])
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["balance"], 
            body
            )
        if result:
            balance = result["data"]["balance"]
            return balance
        else:
            return None

    def order_info_by_order_id(self, order_id: int) -> Dict:
        body = build_dict(self.config["shop_id"], 
            {
            "order_id": order_id
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["order_info"], 
            body
            )
        if result:
            order_info = result["data"]
            return order_info
        else:
            return None

    def order_info_by_payment_id(self, payment_id: str) -> Dict:
        body = build_dict(self.config["shop_id"], 
            {
            "payment_id": payment_id
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["order_info"], 
            body
            )
        if result:
            order_info = result["data"]
            return order_info
        else:
            return None

    def orders_list(self, page: int = 1) -> List[Dict]:
        body = build_dict(self.config["shop_id"], 
            {
            "page": page
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["orders_list"], 
            body
            )
        if result:
            orders = result["data"]
            return orders
        else:
            return None
    
    def withdrawals_list(self, page: int = 1) -> List[Dict]:
        body = build_dict(self.config["shop_id"], 
            {
            "page": page
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["withdrawals_list"], 
            body
            )
        if result:
            withdrawals = result["data"]
            return withdrawals
        else:
            return None
        
    def withdrawal_info_by_order_id(self, order_id: int) -> Dict:
        body = build_dict(self.config["shop_id"], 
            {
            "order_id": order_id
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["withdrawal_info"], 
            body)
        if result:
            withdrawal_info = result["data"]
            return withdrawal_info
        else:
            return None

    def withdrawal_info_by_payment_id(self, payment_id: str) -> Dict:
        body = build_dict(self.config["shop_id"], 
            {
            "payment_id": payment_id
            })
        result = post(
            self.config["shop_id"], 
            self.config["api_key"], 
            self.config["api_url"], 
            self.endpoints["withdrawal_info"], 
            body
            )
        if result:
            withdrawal_info = result["data"]
            return withdrawal_info
        else:
            return None