import requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'


def test_add_product_to_cart_api(cart_add_fixture):
    assert requests.put("http://127.0.0.1:8000/cart/00/1/", json={"user_id": 1, "stock_id": "1"}).json() == {
        "message": "item added to cart successfully"}
    assert requests.put("http://127.0.0.1:8000/cart/00/10/", json={"user_id": 1, "stock_id": "1"}).json() == {
        "message": "item added to cart successfully"}
    assert requests.put("http://127.0.0.1:8000/cart/00/10/", json={"user_id": 1, "stock_id": "1"}).json() == {
        "error": "nothing changed"}
    assert requests.put("http://127.0.0.1:8000/cart/00/0/", json={"user_id": 1, "stock_id": "1"}).json() == {
        "message": "product deleted successfully"}


def test_remove_product_from_cart_api(remove_from_cart_fixture):
    assert requests.delete("http://127.0.0.1:8000/cart/0000/", json={"user_id": 1, "stock_id": "1"}).json() == {
        "message": "product deleted successfully"}
    assert requests.delete("http://127.0.0.1:8000/cart/0000000/", json={"user_id": 1, "stock_id": "1"}).json() == {
        'error': 'product not found'}


def test_get_cart_api(cart_get_fixture):
    assert requests.post("http://127.0.0.1:8000/cart/", json={"user_id": 1}).json() == {'user_id': 1,
                                                                                        'products': [{'count': 1,
                                                                                                      'status': 'in_cart',
                                                                                                      'stock_id': '1',
                                                                                                      'system_code': '0000'}]}
    assert requests.post("http://127.0.0.1:8000/cart/", json={"user_id": 2}).json() == {'error': 'cart not found'}
