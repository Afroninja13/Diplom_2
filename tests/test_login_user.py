import allure
from data import TestData
from helpers import random_word, login_user
from conftest import user_model


class TestLoginUser:

    @allure.title('Проверка логина пользователя с валидными значениями login, password')
    def test_login_user_with_valid_credentials(self, user_model):
        response = login_user(user_model['payload']['email'], user_model['payload']['password'])
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Проверка ошибки логина пользователя c невалидным значением поля email')
    def test_login_user_with_invalid_email_return_error(self, user_model):
        response = login_user(random_word(), user_model['payload']['password'])
        assert response.status_code == 401
        assert response.json()['message'] == TestData.LOGIN_USER_FIELD_ERROR

    @allure.title('Проверка ошибки логина пользователя c невалидным значением поля password')
    def test_login_user_with_invalid_password_return_error(self, user_model):
        response = login_user(user_model['payload']['email'], random_word())
        assert response.status_code == 401
        assert response.json()['message'] == TestData.LOGIN_USER_FIELD_ERROR

    @allure.title('Проверка ошибки логина пользователя c невалидными значениями полей email, password')
    def test_login_user_with_invalid_credentials_return_error(self, user_model):
        response = login_user(random_word(), random_word())
        assert response.status_code == 401
        assert response.json()['message'] == TestData.LOGIN_USER_FIELD_ERROR
