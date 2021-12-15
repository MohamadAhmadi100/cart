"""
Cart
"""

# import requests

from RPC.cart.db_conection.db import MongoDb


class Cart:
    @staticmethod
    def add_to_cart(system_code: str, user_id: int, count: int, new: bool) -> dict:
        """
        Adding product into user cart
        :param new: if its new item True
        :param user_id:
        :param system_code:
        :param count:
        :return: True of False message
        """
        # product = json.loads(requests.request("get", f"alaki.alaki.com/product/{system_code}/").text).update({"count": count})
        product = {"system_code": system_code, "count": count}
        with MongoDb() as client:
            if count < 1:
                return Cart.remove_from_cart(system_code, user_id)
            elif new:
                result = client.cart_collection.update_one({"user_id": user_id},
                                                           {'$addToSet': {'products': product}},
                                                           upsert=True)
            else:
                result = client.cart_collection.update_one({"user_id": user_id, "products.system_code": system_code},
                                                           {"$set": {"products.$.count": count}})
            if not result.raw_result.get("updatedExisting") or result.modified_count:
                return {"message": "item added to cart successfully"}
            return {"error": "nothing changed"}

    @staticmethod
    def get_cart(cart_id: int) -> dict:
        """
        :param cart_id:
        :return: info of cart
        """
        with MongoDb() as client:
            db_find = client.cart_collection.find_one({"user_id": cart_id}, {"_id": 0})
            if db_find:
                return db_find
            return {'error': 'cart not found'}

    @staticmethod
    def remove_from_cart(system_code: str, user_id: int) -> dict:
        """
        :param user_id:
        :param system_code:
        :return: True or False message
        """
        with MongoDb() as client:
            result = client.cart_collection.update_one({"user_id": user_id},
                                                       {"$pull": {"products": {"system_code": system_code}}})
            if result.modified_count:
                return {'message': 'product deleted successfully'}
            return {'error': 'product not found'}
