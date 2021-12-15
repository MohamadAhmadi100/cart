import requests
import os

os.environ['NO_PROXY'] = '127.0.0.1'


def test_add_product_to_cart_api(cart_add_fixture):
    assert requests.put("http://127.0.0.1:8000/cart/00/1/", json={"user_id": 1, "new": True}).json() == {
        "message": "item added to cart successfully"}


def test_remove_product_from_cart_api(remove_from_cart_fixture):
    assert requests.delete("http://127.0.0.1:8000/cart/0000/", json={"user_id": 1}).json() == {
        "message": "product deleted successfully"}


def test_get_cart_api(cart_get_fixture):
    assert requests.post("http://127.0.0.1:8000/cart/", json={"user_id": 1}).json() == {
        "user_id": 1,
        "products": [
            {
                "system_code": "0000",
                "count": 1
            }
        ]
    }
