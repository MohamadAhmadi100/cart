"""
Cart
"""
from typing import Union

from app.models.db_conection.db import MongoDb


class Cart:
    def __init__(self, count: int, storage_id: str, user_info: dict, product: dict):
        self.count = count
        self.storage_id = storage_id
        self.user_info = user_info
        self.product = product
        self.insurance = dict()
        self.shipment = dict()

    def add_to_cart(self) -> Union[str, tuple]:
        """
        Adding product into user cart
        """
        product = {
            "status": "in_cart",
            "count": self.count,
            "storage_id": self.storage_id
        }
        product.update(self.product)
        with MongoDb() as client:
            db_data = client.cart_collection.find_one(
                {"user_info.user_id": self.user_info.get('user_id'),
                 "products.system_code": self.product.get('system_code'),
                 "products.storage_id": self.storage_id})

            if db_data:
                in_cart_count = \
                    [a for a in db_data.get('products') if a.get("system_code") == self.product.get("system_code")][
                        0].get("count")
                if in_cart_count + self.count <= 0:
                    return self.remove_from_cart(self.product.get('system_code'), self.user_info.get('user_id'),
                                                 self.storage_id), "delete"
                result = client.cart_collection.update_one(
                    {"user_info.user_id": self.user_info.get('user_id'),
                     "products": {"$elemMatch": {"system_code": self.product.get('system_code'),
                                                 "storage_id": self.storage_id}}},
                    {"$inc": {"products.$.count": product['count']}})
            else:
                result = client.cart_collection.update_one({"user_info.user_id": self.user_info.get('user_id')},
                                                           {
                                                               "$set": {
                                                                   "shipment": self.shipment,
                                                                   "insurance": self.insurance
                                                               },
                                                               '$addToSet': {'products': product}
                                                            }, upsert=True)
            if not result.raw_result.get("updatedExisting") or result.modified_count:
                return "item edited in cart successfully"
            return "nothing changed", "nothing"

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
