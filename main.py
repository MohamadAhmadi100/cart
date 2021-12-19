"""
FastAPI
"""
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel, validator

from models.cart.cart import Cart

TAGS = [
    {
        "name": "Cart",
        "description": "Cart CRUD"
    }
]

app = FastAPI(
    title="Cart API",
    description="This is Cart MicroService",
    version="0.1.0",
    openapi_tags=TAGS
)


class CartModel(BaseModel):
    user_id: int
    storage_id: str

    @validator("user_id")
    def user_id_validator(cls, value):
        if type(value) is not int:
            raise ValueError("user_id must be int")
        return value

    @validator("storage_id")
    def stock_id_validator(cls, value):
        if type(value) is not str:
            raise ValueError("storage_id must be str")
        return value


class GetCart(BaseModel):
    user_id: int

    @validator("user_id")
    def user_id_validator(cls, value):
        if type(value) is not int:
            raise ValueError("user_id must be int")
        return value


@app.put("/cart/{system_code}/{count}/", status_code=201, tags=["Cart"])
def add_product_to_cart_api(system_code: str, count: int, requestbody: CartModel) -> dict:
    """
    add item to cart
    """
    return Cart.add_to_cart(system_code, requestbody.user_id, count, requestbody.storage_id)


@app.delete("/cart/{system_code}/", status_code=200, tags=["Cart"])
def remove_product_from_cart_api(system_code: str, requestbody: CartModel) -> dict:
    """
    remove an item from cart
    """
    return Cart.remove_from_cart(system_code, requestbody.user_id, requestbody.storage_id)


@app.post("/cart/", status_code=200, tags=["Cart"])
def get_cart_api(item: GetCart) -> dict:
    """
    get user cart
    """
    return Cart.get_cart(item.user_id)


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
