import sys
from fastapi.testclient import TestClient
from app.main import app

sys.path.append("..")

client = TestClient(app)


def test_add_product_to_cart_api(cart_add_fixture):
    response = client.put("/cart/", json={"count": 1,
                                          "storage_id": "1", "price": 600000,
                                          "user_info": {"user_id": 1},
                                          "products": {"system_code": "1"}})
    assert response.status_code == 202
    assert response.json() == {"message": "item added to cart successfully"}

    second_response = client.put("/cart/", json={"count": 10,
                                                 "storage_id": "1", "price": 600000,
                                                 "user_info": {"user_id": 1},
                                                 "products": {"system_code": "1"}})

    assert second_response.status_code == 202
    assert second_response.json() == {"message": "item added to cart successfully"}

    third_response = client.put("/cart/", json={"count": 10,
                                                "storage_id": "1", "price": 600000,
                                                "user_info": {"user_id": 1},
                                                "products": {"system_code": "1"}})

    assert third_response.status_code == 417
    assert third_response.json() == {"error": "nothing changed"}

    fourth_response = client.put("/cart/", json={"count": 0,
                                                 "storage_id": "1", "price": 600000,
                                                 "user_info": {"user_id": 1},
                                                 "products": {"system_code": "1"}})

    assert fourth_response.status_code == 200
    assert fourth_response.json() == {'message': 'product deleted successfully'}


def test_remove_product_from_cart_api(delete_fixture):
    response = client.delete("/cart/1/1/1")
    assert response.status_code == 200
    assert response.json() == {'message': 'product deleted successfully'}

    second_response = client.delete("/cart/1/1/1")
    assert second_response.status_code == 404
    assert second_response.json() == {'error': 'product not found'}


def test_get_cart_api(delete_fixture):
    response = client.get("/cart/1/")
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'user_info': {'user_id': 1}, 'products': [
        {'status': 'in_cart', 'count': 1, 'storage_id': '1', 'price': 600000, 'system_code': '1'}]}

    response = client.get("/cart/2/")
    assert response.status_code == 404
    assert response.json() == {'error': 'cart not found'}
