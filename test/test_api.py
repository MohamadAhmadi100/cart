import sys

from app.controllers.cart_controller import get_cart, add_and_edit_product_in_cart, remove_product_from_cart

sys.path.append("..")


def test_add_product_to_cart_api(cart_add_fixture):
    response = add_and_edit_product_in_cart(**{'user_info': {'user_id': 'test'},
                                               'product': {'system_code': '100104001018', 'visible_in_site': True,
                                                           'config': {'storage': {'value': '64 GB',
                                                                                  'attribute_label': 'حافظه داخلی',
                                                                                  'label': '۶۴ گیگابایت'},
                                                                      'color': {'value': 'blue',
                                                                                'attribute_label': 'رنگ',
                                                                                'label': 'آبی'},
                                                                      'guarantee': {'value': 'awat',
                                                                                    'attribute_label': 'گارانتی',
                                                                                    'label': 'آوات'},
                                                                      'ram': {'value': '4 GB', 'attribute_label': 'رم',
                                                                              'label': '۴ گیگابایت'},
                                                                      'seller': {'value': 'Awat',
                                                                                 'attribute_label': 'فروشنده',
                                                                                 'label': 'آوات'}}}, 'price': 50000000,
                                               'count': 1, 'storage_id': '1'})
    assert response.get('status_code') == 201
    assert response.get('message') == "item added to cart successfully"

    second_response = add_and_edit_product_in_cart(**{'user_info': {'user_id': 'test'},
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

    assert second_response.get('status_code') == 201
    assert second_response.get('message') == "item added to cart successfully"

    third_response = add_and_edit_product_in_cart(**{'user_info': {'user_id': 'test'},
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

    assert third_response.get('status_code') == 417
    assert third_response.get('message') == "nothing changed"

    fourth_response = add_and_edit_product_in_cart(**{'user_info': {'user_id': 'test'},
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
                                                      'count': 0, 'storage_id': '1'})

    assert fourth_response.get('status_code') == 200
    assert fourth_response.get('message') == 'product deleted successfully'


def test_remove_product_from_cart_api(delete_fixture):
    response = remove_product_from_cart('100104001018', 'test', '1')
    assert response.get("status_code") == 200
    assert response.get("message") == 'product deleted successfully'

    second_response = remove_product_from_cart('100104001018', 'test', '1')
    assert second_response.get("status_code") == 404
    assert second_response.get("error") == 'product not found'


def test_get_cart_api(delete_fixture):
    response = get_cart('test')
    assert response.get("status_code") == 200
    assert response.get("message") == {'products': [{'config': {'color': {'attribute_label': 'رنگ',
                                                                          'label': 'آبی',
                                                                          'value': 'blue'},
                                                                'guarantee': {'attribute_label': 'گارانتی',
                                                                              'label': 'آوات',
                                                                              'value': 'awat'},
                                                                'ram': {'attribute_label': 'رم',
                                                                        'label': '۴ گیگابایت',
                                                                        'value': '4 GB'},
                                                                'seller': {'attribute_label': 'فروشنده',
                                                                           'label': 'آوات',
                                                                           'value': 'Awat'},
                                                                'storage': {'attribute_label': 'حافظه داخلی',
                                                                            'label': '۶۴ گیگابایت',
                                                                            'value': '64 GB'}},
                                                     'count': 10,
                                                     'price': 50000000,
                                                     'status': 'in_cart',
                                                     'storage_id': '1',
                                                     'system_code': '100104001018',
                                                     'visible_in_site': True}],
                                       'user_info': {'user_id': 'test'}}

    second_response = get_cart('test2')
    assert second_response.get("status_code") == 404
    assert second_response.get("error") == 'cart not found'
