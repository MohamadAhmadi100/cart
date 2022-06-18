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
            return {"success": True, "status_code": 200, "message": message,
                    "cart": Cart.get_cart(user_info.get("user_id"))}
        return {"success": False, "status_code": 417, "message": message}
    return {"success": True, "status_code": 201, "message": response, "cart": Cart.get_cart(user_info.get("user_id"))}


def remove_product_from_cart(system_code: str, user_id: int, storage_id: str) -> dict:
    """
    remove an item from cart
    """
    response = Cart.remove_from_cart(system_code, user_id, storage_id)
    if response:
        return {"success": True, "status_code": 200, "message": response,
                "cart": Cart.get_cart(user_id)}
    return {'success': False, 'status_code': 404, 'error': 'product not found'}


def get_cart(user_id: int) -> dict:
    """
    get user cart
    """
    stored_data = Cart.get_cart(user_id)
    return {"success": True, "status_code": 200, "message": stored_data}


def add_shipment_to_cart(shipment):
    """
    add shipment info to user's cart
    """
    stored_data = Cart.add_shipment(user_id=shipment.get("user_id"), shipment_details=shipment.get("shipment_details"))
    if stored_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def add_wallet_to_cart(user_id: int, wallet_amount: int):
    """
    add wallet info to user's cart
    """
    stored_data = Cart.add_wallet(user_id, wallet_amount)
    if stored_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def add_payment_to_cart(user_id: int, payment_method: str):
    """
    add payment info to user's cart
    """
    stored_data = Cart.add_payment(user_id, payment_method)
    if stored_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def remove_cart(user_id: int):
    """
    remove shipment, insurance, wallet, payment and coupon
    """
    removed_data = Cart.remove_all_data(user_id)
    if removed_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def add_official_unofficial(user_id: int, customer_detail: object):
    """
    add payment info to user's cart
    """
    stored_data = Cart.add_selected_payment_method(user_id, customer_detail)
    if stored_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def remove_wallet(user_id: int):
    """
    remove shipment, insurance, wallet, payment and coupon
    """
    removed_data = Cart.remove_wallet(user_id)
    if removed_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def delete_cart(user_id: int):
    """
    remove shipment, insurance, wallet, payment and coupon
    """
    removed_data = Cart.remove_cart(user_id)
    if removed_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}


def final_flag(user_id: int):
    """
    add final flag true to cart
    """
    removed_data = Cart.add_payment_flag(user_id)
    if removed_data is not None:
        return {"success": True, "message": "عملیات موفق بود"}
    return {"success": False, "message": "عملیات ناموفق بود"}
