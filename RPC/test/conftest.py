import pytest
from RPC.cart.db_conection.db import MongoDb
from RPC.cart.cart import Cart


@pytest.fixture
def cart_add_fixture():
    yield
    with MongoDb() as client:
        client.cart_collection.delete_one({'user_id': 1})


@pytest.fixture
def cart_get_fixture():
    Cart.add_to_cart("0000", 1, 1, new=True)
    yield
    with MongoDb() as client:
        client.cart_collection.delete_one({'user_id': 1})


@pytest.fixture
def remove_from_cart_fixture():
    Cart.add_to_cart("0000", 1, 1, new=True)
    Cart.add_to_cart("00000", 1, 1, new=True)
    yield
    with MongoDb() as client:
        client.cart_collection.delete_one({'user_id': 1})
