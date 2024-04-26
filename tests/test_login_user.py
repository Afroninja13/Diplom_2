import pytest
import allure
from data import TestData
from helpers import random_word, login_user, create_user, delete_user


class TestLoginUser:
    access_token = None
    email = random_word()
    password = random_word()
    name = random_word()

    def setup_class(self):
        response = create_user(self.email, self.password, self.name)
        self.access_token = response.json()['accessToken']

    def teardown_class(self):
        delete_user(self.access_token)

    @allure.title('Проверка логина пользователя с валидными значениями login, password')
    def test_login_user_with_valid_credentials(self):
        response = login_user(self.email, self.password)
        assert response.status_code == 200
        assert response.json()['success'] is True

    @allure.title('Проверка ошибки логина пользователя c невалидными значениями полей email, password')
    @pytest.mark.parametrize('email, password', [(email, random_word()),
                                                 (random_word(), password),
                                                 (random_word(), random_word())])
    def test_login_user_with_invalid_credentials_return_error(self, email, password):
        response = login_user(email, password)
        assert response.status_code == 401
        assert response.json()['message'] == TestData.LOGIN_USER_FIELD_ERROR
