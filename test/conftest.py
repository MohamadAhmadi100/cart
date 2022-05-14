import pytest

from app.controllers.cart_controller import add_and_edit_product_in_cart
from app.models.db_conection.db import MongoDb


@pytest.fixture
def cart_add_fixture():
    yield
    with MongoDb() as mongo:
        mongo.cart_collection.delete_one({'user_info.user_id': 'test'})


@pytest.fixture
def delete_fixture():
    add_and_edit_product_in_cart(**{'user_info': {'user_id': 'test'},
                                    'product': {'system_code': '100104001018',
                                                'visible_in_site': True,
                                                'config': {'storage': {'value': '64 GB',
                                                                       'attribute_label': 'حافظه داخلی',
                                                                       'label': '۶۴ گیگابایت'},
                                                           'color': {'value': 'blue',
                                                                     'attribute_label': 'رنگ',
                                                                     'label': 'آبی'},
                                                           'guarantee': {'value': 'awat',
                                                                         'attribute_label': 'گارانتی',
                                                                         'label': 'آوات'},
                                                           'ram': {'value': '4 GB',
                                                                   'attribute_label': 'رم',
                                                                   'label': '۴ گیگابایت'},
                                                           'seller': {'value': 'Awat',
                                                                      'attribute_label': 'فروشنده',
                                                                      'label': 'آوات'}}},
                                    'price': 50000000,
                                    'count': 10, 'storage_id': '1'})
    yield
    with MongoDb() as mongo:
        mongo.cart_collection.delete_one({'user_info.user_id': 'test'})
