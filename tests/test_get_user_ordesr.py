import allure
from data import TestData
from helpers import create_order, get_ingredients_data, get_user_orders
from conftest import user_model


class TestGetUserOrders:

    @allure.title('Проверка получения заказов пользователя с авторизацией')
    def test_get_user_orders_with_authorization(self, user_model):
        ingredients_data = get_ingredients_data().json()
        ingredients_id_list = [ingredients_data['data'][0]['_id']]
        create_order(ingredients_id_list, user_model['response_create'].json()['accessToken'])
        response = get_user_orders(user_model['response_create'].json()['accessToken'])
        assert response.status_code == 200
        assert response.json()['orders'] is not None

    @allure.title('Проверка ошибки при получении заказов пользователя без авторизации')
    def test_get_user_orders_without_authorization(self):
        response = get_user_orders(None)
        assert response.status_code == 401
        assert response.json()['message'] == TestData.AUTH_ERROR
