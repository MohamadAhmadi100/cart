from fastapi import APIRouter, HTTPException, Response
from app.models.cart import Cart

router = APIRouter()


@router.put("/cart/", status_code=202, tags=["Cart"])
def edit_and_add_product_in_cart(item: Cart, responses: Response) -> dict:
    """
    edit and add item in cart
    """
    response = item.add_to_cart()
    if type(response) is tuple:
        message, status = response
        if status == 'delete':
            responses.status_code = 200
            return message
        raise HTTPException(status_code=417, detail=message)
    return response


@router.delete("/cart/{system_code}/{user_id}/{storage_id}", status_code=200, tags=["Cart"])
def remove_product_from_cart(system_code: str, user_id: int, storage_id: str) -> dict:
    """
    remove an item from cart

    """
    response = Cart.remove_from_cart(system_code, user_id, storage_id)
    if response:
        return response
    raise HTTPException(status_code=404, detail={'error': 'product not found'})


@router.get("/cart/{user_id}/", status_code=200, tags=["Cart"])
def get_cart(user_id: int) -> dict:
    """
    get user cart
    """
    cart = Cart.construct()
    stored_data = cart.get_cart(user_id)
    if stored_data:
        return stored_data.dict()
    raise HTTPException(status_code=404, detail={'error': 'cart not found'})
