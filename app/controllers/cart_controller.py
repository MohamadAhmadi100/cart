from app.models.cart import Cart


def add_and_edit_product_in_cart(count: int, storage_id: str, user_info: dict, product: dict) -> dict:
    """
    edit and add item in cart
    """
    cart = Cart(count, storage_id, user_info, product)
    response = cart.add_to_cart()
    if type(response) is tuple:
        message, status = response
        if status == 'delete':
            return {"success": True, "status_code": 200, "message": message}
        return {"success": False, "status_code": 417, "message": message}
    return {"success": True, "status_code": 201, "message": response}


def remove_product_from_cart(system_code: str, user_id: int, storage_id: str) -> dict:
    """
    remove an item from cart
    """
    response = Cart.remove_from_cart(system_code, user_id, storage_id)
    if response:
        return {"success": True, "status_code": 200, "message": response}
    return {'success': False, 'status_code': 404, 'error': 'product not found'}


def get_cart(user_id: int) -> dict:
    """
    get user cart
    """
    stored_data = Cart.get_cart(user_id)
    if stored_data:
        return {"success": True, "status_code": 200, "message": stored_data}
    return {'success': False, 'status_code': 404, 'error': 'cart not found'}
