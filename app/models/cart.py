"""
Cart
"""
from typing import Union

from app.models.db_conection.db import MongoDb


class Cart:
    def __init__(self, count: int, storage_id: str, price: int, user_info: dict, product: dict):
        self.count = count
        self.storage_id = storage_id
        self.price = price
        self.user_info = user_info
        self.product = product
        self.insurance = list()
        self.shipment = list()

    def add_to_cart(self) -> Union[str, tuple]:
        """
        Adding product into user cart
        """
        product = {
            "status": "in_cart",
            "count": self.count,
            "storage_id": self.storage_id,
            "price": self.price,
            "insurance": self.insurance,
            "shipment": self.shipment,
        }
        product.update(self.product)
        with MongoDb() as client:
            db_data = client.cart_collection.find_one(
                {"user_info.user_id": self.user_info.get('user_id'),
                 "products.system_code": self.product.get('system_code'),
                 "products.storage_id": self.storage_id})
            if self.count < 1:
                return Cart.remove_from_cart(self.product.get('system_code'), self.user_info.get('user_id'),
                                             self.storage_id), "delete"
            elif db_data:
                result = client.cart_collection.update_one(
                    {"user_info.user_id": self.user_info.get('user_id'),
                     "products": {"$elemMatch": {"system_code": self.product.get('system_code'),
                                                 "storage_id": self.storage_id}}},
                    {"$set": {"products.$": product}})
            else:
                result = client.cart_collection.update_one({"user_info.user_id": self.user_info.get('user_id')},
                                                           {'$addToSet': {'products': product}},
                                                           upsert=True)
            if not result.raw_result.get("updatedExisting") or result.modified_count:
                return "item added to cart successfully"
            return "nothing changed", "error"

    @staticmethod
    def get_cart(cart_id: int):
        """
        getting cart
        """
        with MongoDb() as client:
            db_find = client.cart_collection.find_one({"user_info.user_id": cart_id}, {"_id": 0})
            if db_find:
                return db_find
            return None

    @staticmethod
    def remove_from_cart(system_code: str, user_id: int, storage_id: str) -> Union[str, None]:
        """
        removing product from cart
        """
        with MongoDb() as client:
            result = client.cart_collection.update_one({"user_info.user_id": user_id},
                                                       {"$pull": {"products": {"system_code": system_code,
                                                                               "storage_id": storage_id}}})
            if result.modified_count:
                return 'product deleted successfully'
            return None
