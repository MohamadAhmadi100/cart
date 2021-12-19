from models.cart.cart import Cart


def test_cart_add(cart_add_fixture):
    assert Cart.add_to_cart("00", 1, 1, "1")["message"] == 'item added to cart successfully'
    assert Cart.add_to_cart("00", 1, 1, "1")["error"] == 'nothing changed'
    assert Cart.add_to_cart("00", 1, 5, "1")["message"] == 'item added to cart successfully'
    assert Cart.add_to_cart("00", 1, 1, "1")["message"] == 'item added to cart successfully'
    assert Cart.add_to_cart("00", 1, 0, "1")["message"] == 'product deleted successfully'


def test_get_cart(cart_get_fixture):
    assert Cart.get_cart(1) == {'user_id': 1,
                                'products': [{'count': 1, 'status': 'in_cart', 'stock_id': '1', 'system_code': '0000'}]}
    assert Cart.get_cart(2)["error"] == 'cart not found'


def test_remove_from_cart(remove_from_cart_fixture):
    assert Cart.remove_from_cart("00000", 1, "1")["message"] == 'product deleted successfully'
    assert Cart.remove_from_cart("00000", 1, "1")["error"] == 'product not found'
