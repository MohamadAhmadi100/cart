import pytest
from app.models.db_conection.db import MongoDb
from test.test_api import client


@pytest.fixture
def cart_add_fixture():
    yield
    with MongoDb() as mongo:
        mongo.cart_collection.delete_one({'user_info.user_id': 1})


@pytest.fixture
def delete_fixture():
    client.put("/cart/", json={"count": 1, "storage_id": "1", "price": 600000, "user_info": {"user_id": 1},
                               "products": {"system_code": "1"}})
    yield
    with MongoDb() as mongo:
        mongo.cart_collection.delete_one({'user_info.user_id': 1})
