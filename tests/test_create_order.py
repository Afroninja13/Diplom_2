import pytest
import allure
from data import TestData
from helpers import random_word, create_user, delete_user, create_order, get_ingredients_data, get_user_orders


class TestCreateOrder:

    def setup_method(self):
        self.email = random_word()
        self.password = random_word()
        self.name = random_word()
        response_create = create_user(self.email, self.password, self.name)
        self.access_token = response_create.json()['accessToken']
        self.ingredients_id_list = []

    def teardown_method(self):
        delete_user(self.access_token)

    @allure.title('Проверка создания заказа с авторизацией')
    def test_create_order_with_authorization(self):
        ingredients_data = get_ingredients_data().json()
        self.ingredients_id_list.append(ingredients_data['data'][0]['_id'])
        response_create = create_order(self.ingredients_id_list, self.access_token)
        assert response_create.status_code == 200
        assert response_create.json()['name'] == 'Флюоресцентный бургер'
        assert len(get_user_orders(self.access_token).json()['orders']) == 1

    @pytest.mark.xfail(reason='Баг. Заказ создается без авторизации, что противоречит API доке.')
    @allure.title('Проверка создания заказа без авторизации')
    def test_create_order_without_authorization(self):
        ingredients_data = get_ingredients_data().json()
        self.ingredients_id_list.append(ingredients_data['data'][0]['_id'])
        response_create = create_order(self.ingredients_id_list, None)
        assert response_create.status_code == 401
        assert response_create.json()['message'] == TestData.AUTH_ERROR
        assert len(get_user_orders(self.access_token).json()['orders']) == 0

    @allure.title('Проверка создания заказа без ингредиентов')
    def test_create_order_without_ingredients(self):
        response_create = create_order(None, self.access_token)
        assert response_create.status_code == 400
        assert response_create.json()['message'] == TestData.NO_INGREDIENTS_ERROR
        assert len(get_user_orders(self.access_token).json()['orders']) == 0

    @allure.title('Проверка создания заказа c неверным хешем ингредиента')
    def test_create_order_with_invalid_ingredients_hash(self):
        self.ingredients_id_list.append(random_word())
        response_create = create_order(self.ingredients_id_list, self.access_token)
        assert response_create.status_code == 500
        assert len(get_user_orders(self.access_token).json()['orders']) == 0
        