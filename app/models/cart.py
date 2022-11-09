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
                if not result.raw_result.get("updatedExisting") or result.modified_count:
                    if self.count > 0:
                        return "محصول به سبد خرید اضافه شد"
                    else:
                        return "محصول در سبد خرید کاهش داده شد"
            else:
                result = client.cart_collection.update_one({"user_info.user_id": self.user_info.get('user_id')},
                                                           {
                                                               "$set": {
                                                                   "shipment": self.shipment,
                                                               },
                                                               '$addToSet': {'products': product}
                                                           }, upsert=True)
                if not result.raw_result.get("updatedExisting") or result.modified_count:
                    return "محصول به سبد خرید اضافه شد"
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
            return {"user_info.user_id": cart_id, "products": []}

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
                return 'محصول از سبد خرید حذف شد'
            return None

    @staticmethod
    def basket_add_to_cart(user_id, basket_id, basket_data):
        with MongoDb() as mongo:
            result = mongo.cart_collection.update_one(
                {"user_info.user_id": user_id},
                {"$push": {f"baskets.{basket_id}": basket_data},
                 "$setOnInsert": {"products": [],
                                  "shipment": {}
                                  }
                 },
                upsert=True
            )
            if result.modified_count or result.upserted_id:
                return True
            return False

    @staticmethod
    def edit_basket_cart(user_id, basket_id, basket_data, list_index):
        with MongoDb() as mongo:
            result = mongo.cart_collection.update_one(
                {"user_info.user_id": user_id},
                {"$set": {f"baskets.{basket_id}.{list_index}": basket_data}},
            )
            if result.modified_count or result.upserted_id:
                return True
            return False

    @staticmethod
    def add_shipment(user_id: int, shipment_details: dict):
        """
        add shipment details to customer's cart and change cart's amount
        """
        try:
            with MongoDb() as client:
                storage = list(shipment_details.keys())[0]
                client.cart_collection.update_one({"user_info.user_id": user_id},
                                                  {"$set": {f"shipment.{storage}": shipment_details[storage]}})
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def add_wallet(user_id: int, wallet_amount: int):
        """
        When customers use their wallet, details save on their cart
        """
        try:
            with MongoDb() as client:
                client.cart_collection.update_one({"user_info.user_id": user_id},
                                                  {"$set": {"payment.walletAmount": wallet_amount}})
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def add_payment(user_id: int, payment_method: str):
        """
        When customers use their payment, details save on their cart
        """
        try:
            with MongoDb() as client:
                client.cart_collection.update_one({"user_info.user_id": user_id},
                                                  {"$set": {"payment.paymentMethod": payment_method}})
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def remove_all_data(user_id: int):
        """
        re-initial cart and remove objects of wallet, shipment, insurance,...
        """
        try:
            with MongoDb() as client:
                cart = client.cart_collection.find({"user_info.user_id": user_id})
                for root_cart in cart:
                    if root_cart.get("unofficial") is not None:
                        del root_cart['unofficial']
                    root_cart['shipment'], root_cart['payment'], root_cart['coupon'] = {}, {}, {}
                    client.cart_collection.replace_one({"user_info.user_id": user_id},
                                                       root_cart)
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def add_selected_payment_method(user_id, customer_detial):
        """
        When customers select unofficial order, details save on their cart
        """
        try:
            with MongoDb() as client:
                client.cart_collection.update_one({"user_info.user_id": user_id},
                                                  {"$set": {"informal": customer_detial}})
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    def remove_wallet(user_id: int):
        """
        re-initial cart and remove objects of wallet, shipment, insurance,...
        """
        try:
            with MongoDb() as client:
                cart = client.cart_collection.find({"user_info.user_id": user_id})
                for root_cart in cart:
                    if root_cart['payment'].get("walletAmount") is not None:
                        del root_cart['payment']['walletAmount']
                    client.cart_collection.replace_one({"user_info.user_id": user_id},
                                                       root_cart)
                return "موفق"
        except:
            return None

    @staticmethod
    def remove_cart(user_id: int):
        """
        re-initial cart and remove objects of wallet, shipment, insurance,...
        """
        try:
            with MongoDb() as client:
                client.cart_collection.delete_one({"user_info.user_id": int(user_id)})
                return "موفق"
        except:
            return None

    @staticmethod
    def add_payment_flag(user_id: int):
        """
        add payment flag to cart
        """
        try:
            with MongoDb() as client:
                client.cart_collection.update_one({"user_info.user_id": user_id},
                                                  {"$set": {"finalFlag": True}})
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def remove_all_data_callback(user_id: int):
        """
        re-initial cart and remove objects of wallet, shipment, insurance,...
        """
        try:
            with MongoDb() as client:
                cart = client.cart_collection.find({"user_info.user_id": user_id})
                for root_cart in cart:
                    del root_cart['finalFlag']
                    if root_cart.get("unofficial") is not None:
                        del root_cart['unofficial']

                    root_cart['shipment'], root_cart['payment'], root_cart['coupon'] = {}, {}, {}
                    client.cart_collection.replace_one({"user_info.user_id": user_id},
                                                       root_cart)
                return "اطلاعات با موفقیت اضافه شد"
        except:
            return None

    @staticmethod
    def replace_baskets(user_id: int, baskets: list):
        try:
            with MongoDb() as client:
                client.cart_collection.update_one({"user_info.user_id": user_id}, {"$set": {"baskets": baskets}})
                return {"success": True}
        except:
            return {"success": False}
