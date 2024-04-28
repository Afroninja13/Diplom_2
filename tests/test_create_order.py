import pytest
import allure
from data import TestData
from helpers import random_word, create_order, get_user_orders
from conftest import user_model, order_model


class TestCreateOrder:

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_authorization(self, user_model, order_model):
        response_create = create_order(order_model['ingredients_id_list'],
                                       user_model['response_create'].json()['accessToken'])
        assert response_create.status_code == 200
        assert response_create.json()['name'] == 'Флюоресцентный бургер'
        assert len(get_user_orders(user_model['response_create'].json()['accessToken']).json()['orders']) == 1

    @pytest.mark.xfail(reason='Баг. Заказ создается без авторизации, что противоречит API доке.')
    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_authorization(self, user_model, order_model):

        response_create = create_order(order_model['ingredients_id_list'], None)
        assert response_create.status_code == 401
        assert response_create.json()['message'] == TestData.AUTH_ERROR
        assert len(get_user_orders(user_model['response_create'].json()['accessToken']).json()['orders']) == 0

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self, user_model):
        response_create = create_order(None, user_model['response_create'].json()['accessToken'])
        assert response_create.status_code == 400
        assert response_create.json()['message'] == TestData.NO_INGREDIENTS_ERROR
        assert len(get_user_orders(user_model['response_create'].json()['accessToken']).json()['orders']) == 0

    @allure.title('Проверка создания заказа c неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredients_hash(self, user_model, order_model):
        ingredients_fake_list = [random_word()]
        response_create = create_order(ingredients_fake_list,
                                       user_model['response_create'].json()['accessToken'])
        assert response_create.status_code == 500
        assert len(get_user_orders(user_model['response_create'].json()['accessToken']).json()['orders']) == 0
