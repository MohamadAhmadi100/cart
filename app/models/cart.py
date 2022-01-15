"""
Cart
"""
from typing import Union

from fastapi import HTTPException
from pydantic import BaseModel, validator

from app.models.db_conection.db import MongoDb


class Cart(BaseModel):
    count: int
    storage_id: str
    price: int
    user_info: dict
    products: dict

    @validator("storage_id")
    def stock_id_validator(cls, value):
        if not isinstance(value, str):
            raise HTTPException(status_code=422, detail={"error": "storage_id must be str"})
        return value

    @validator("count")
    def count_validator(cls, value):
        if not isinstance(value, int):
            raise HTTPException(status_code=422, detail={"error": "count must be int"})
        elif 0 > value:
            raise HTTPException(status_code=422, detail={"error": "count cant be less than 0"})
        return value

    @validator("price")
    def price_validator(cls, value):
        if not isinstance(value, int):
            raise HTTPException(status_code=422, detail={"error": "price must be int"})
        return value

    @validator("user_info")
    def user_info_validator(cls, value):
        if not isinstance(value, dict):
            raise HTTPException(status_code=422, detail={"error": "user_info must be dict"})
        elif 'user_id' not in value.keys():
            raise HTTPException(status_code=422, detail={"error": "user_id must be a key of user_info"})
        return value

    @validator("products")
    def product_validator(cls, value):
        if not isinstance(value, dict):
            raise HTTPException(status_code=422, detail={"error": "products must be int"})
        elif 'system_code' not in value.keys():
            raise HTTPException(status_code=422, detail={"error": "system_code must be a key of products"})
        return value

    class Config:
        schema_extra = {
            "example": {
                "user_info": {
                    "user_id": 0
                },
                'products': {
                    "system_code": "111"
                },
                "count": 1,
                "storage_id": '1',
                "price": 0

            }
        }

    def add_to_cart(self) -> Union[dict, tuple]:
        """
        Adding product into user cart
        """
        product = {"status": "in_cart", "count": self.count, "storage_id": self.storage_id,
                   "price": self.price}
        product.update(self.products)
        with MongoDb() as client:
            db_data = client.cart_collection.find_one(
                {"user_info.user_id": self.user_info.get('user_id'),
                 "products.system_code": self.products.get('system_code'),
                 "products.storage_id": self.storage_id})
            if self.count < 1:
                return Cart.remove_from_cart(self.products.get('system_code'), self.user_info.get('user_id'),
                                             self.storage_id), "delete"
            elif db_data:
                result = client.cart_collection.update_one(
                    {"user_info.user_id": self.user_info.get('user_id'),
                     "products": {"$elemMatch": {"system_code": self.products.get('system_code'),
                                                 "storage_id": self.storage_id}}},
                    {"$set": {"products.$": product}})
            else:
                result = client.cart_collection.update_one({"user_info.user_id": self.user_info.get('user_id')},
                                                           {'$addToSet': {'products': product}},
                                                           upsert=True)
            if not result.raw_result.get("updatedExisting") or result.modified_count:
                return {"message": "item added to cart successfully"}
            return {"error": "nothing changed"}, "error"

    def get_cart(self, cart_id: int):
        """
        getting cart
        """
        with MongoDb() as client:
            db_find = client.cart_collection.find_one({"user_info.user_id": cart_id}, {"_id": 0})
            if db_find:
                for key in db_find:
                    setattr(self, key, db_find[key])
                return self
            return None

    @staticmethod
    def remove_from_cart(system_code: str, user_id: int, storage_id: str) -> Union[dict, None]:
        """
        removing product from cart
        """
        with MongoDb() as client:
            result = client.cart_collection.update_one({"user_info.user_id": user_id},
                                                       {"$pull": {"products": {"system_code": system_code,
                                                                               "storage_id": storage_id}}})
            if result.modified_count:
                return {'message': 'product deleted successfully'}
            return None
