import allure
from data import TestData
from helpers import random_word, create_user, delete_user, create_order, get_ingredients_data, get_user_orders


class TestGetUserOrders:

    def setup_class(self):
        self.email = random_word()
        self.password = random_word()
        self.name = random_word()
        response_create = create_user(self.email, self.password, self.name)
        self.access_token = response_create.json()['accessToken']
        self.ingredients_id_list = []

    def teardown_class(self):
        delete_user(self.access_token)

    @allure.title('Проверка получения заказов пользователя с авторизацией')
    def test_get_user_orders_with_authorization(self):
        ingredients_data = get_ingredients_data().json()
        self.ingredients_id_list.append(ingredients_data['data'][0]['_id'])
        create_order(self.ingredients_id_list, self.access_token)
        response = get_user_orders(self.access_token)
        assert response.status_code == 200
        assert response.json()['orders'] is not None

    @allure.title('Проверка ошибки при получении заказов пользователя без авторизации')
    def test_get_user_orders_without_authorization(self):
        response = get_user_orders(None)
        assert response.status_code == 401
        assert response.json()['message'] == TestData.AUTH_ERROR
