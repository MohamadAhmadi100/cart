"""
FastAPI
"""
from fastapi import FastAPI
import uvicorn
from RPC.cart.cart import Cart
from pydantic import BaseModel
from pydantic import validator

tags = [
    {
        "name": "Cart",
        "description": "Cart CRUD"
    }
]

app = FastAPI(
    title="Cart API",
    description="This is Cart MicroService",
    version="0.1.0",
    openapi_tags=tags
)


class CartModel(BaseModel):
    user_id: int

    @validator("user_id")
    def user_info_validator(cls, value):
        if type(value) != int:
            raise ValueError("user_info must be int")
        return value


class CartModelAdd(BaseModel):
    user_id: int
    new: bool

    @validator("user_id")
    def user_info_validator(cls, value):
        if type(value) != int:
            raise ValueError("user_info must be int")
        return value

    @validator("new")
    def new_validator(cls, value):
        if type(value) != bool:
            raise ValueError("new must be bool")
        return value


@app.put("/cart/{system_code}/{count}/", status_code=201, tags=["Cart"])
def add_product_to_cart_api(system_code: str, count: int, requestbody: CartModelAdd) -> dict:
    """
    add item to cart
    """
    return Cart.add_to_cart(system_code, requestbody.user_id, count, requestbody.new)


@app.delete("/cart/{system_code}/", status_code=200, tags=["Cart"])
def remove_product_from_cart_api(system_code: str, item: CartModel) -> dict:
    """
    remove an item from cart
    :param system_code:
    :param item: user id
    :return: json object
    """
    return Cart.remove_from_cart(system_code, item.user_id)


@app.post("/cart/", status_code=200, tags=["Cart"])
def get_cart_api(item: CartModel) -> dict:
    """
    get user cart
    :param item:
    :return: json oject
    """
    return Cart.get_cart(item.user_id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
