"""
Cart
"""

# import requests

from models.cart.db_conection.db import MongoDb


class Cart:
    @staticmethod
    def add_to_cart(system_code: str, user_id: int, count: int, storage_id: str) -> dict:
        """
        Adding product into user cart
        """
        # product = json.loads(requests.request("get", f"alaki.alaki.com/product/{system_code}/").text).update({"count": count})
        product = {"status": "in_cart", "system_code": system_code, "count": count, "storage_id": storage_id}
        with MongoDb() as client:
            db_data = client.cart_collection.find_one(
                {"user_id": user_id, "products.system_code": system_code, "products.storage_id": storage_id})
            if count < 1:
                return Cart.remove_from_cart(system_code, user_id, storage_id)
            elif db_data:
                result = client.cart_collection.update_one(
                    {"user_id": user_id,
                     "products": {"$elemMatch": {"system_code": system_code, "storage_id": storage_id}}},
                    {"$set": {"products.$": product}})
            else:
                result = client.cart_collection.update_one({"user_id": user_id},
                                                           {'$addToSet': {'products': product}},
                                                           upsert=True)
            if not result.raw_result.get("updatedExisting") or result.modified_count:
                return {"message": "item added to cart successfully"}
            return {"error": "nothing changed"}
            # else:
            #     # result = client.cart_collection.update_one(
            #     #     {"user_id": user_id,
            #     #      "products": {"$elemMatch": {"system_code": system_code, "storage_id": storage_id}}},
            #     #     {"$cond": {"if": "", "then": "", "else": ""}}, upsert=True)

    @staticmethod
    def get_cart(cart_id: int) -> dict:
        """
        getting cart
        """
        with MongoDb() as client:
            db_find = client.cart_collection.find_one({"user_id": cart_id}, {"_id": 0})
            if db_find:
                return db_find
            return {'error': 'cart not found'}

    @staticmethod
    def remove_from_cart(system_code: str, user_id: int, storage_id: str) -> dict:
        """
        removing product from cart
        """
        with MongoDb() as client:
            result = client.cart_collection.update_one({"user_id": user_id},
                                                       {"$pull": {"products": {"system_code": system_code,
                                                                               "storage_id": storage_id}}})
            if result.modified_count:
                return {'message': 'product deleted successfully'}
            return {'error': 'product not found'}
