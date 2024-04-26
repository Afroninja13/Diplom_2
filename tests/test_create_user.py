import pytest
import requests
import allure
from data import TestData
from helpers import random_word, login_user, create_user, delete_user


class TestCreateUser:
    access_token = None

    def setup_method(self):
        self.email = random_word()
        self.password = random_word()
        self.name = random_word()

    def teardown_method(self):
        delete_user(self.access_token)

    @allure.title('Проверка создания пользователя c валидными значениями login, password, name')
    def test_create_user_with_valid_credentials(self):
        response_create = create_user(self.email, self.password, self.name)
        response_login = login_user(self.email, self.password)
        self.access_token = response_create.json()['accessToken']
        assert response_create.status_code == 200 and response_create.json()['success'] is True
        assert response_login.status_code == 200 and response_login.json()['success'] is True

    @allure.title('Проверка ошибки создания пользователя c занятыми login, password, name')
    def test_create_double_user_returns_error(self):
        response_first = create_user(self.email, self.password, self.name)
        self.access_token = response_first.json()['accessToken']
        response_second = create_user(self.email, self.password, self.name)
        assert response_second.status_code == 403
        assert response_second.json()['message'] == TestData.CREATE_USER_EXIST_ERROR

    @allure.title('Проверка ошибки создания пользователя без одного из обязательных полей email, password, name')
    @pytest.mark.parametrize('payload', [
        ({'email': random_word(), 'password': '', 'name': random_word()}),
        ({'email': random_word(), 'name': random_word()}),
        ({'email': '', 'password': random_word(), 'name': random_word()}),
        ({'password': random_word(), 'name': random_word()}),
        ({'email': random_word(), 'password': random_word(), 'name': ''}),
        ({'email': random_word(), 'password': random_word()}),
    ])
    def test_create_user_without_one_field_returns_error(self, payload):
        response = requests.post(TestData.BASE_URL + TestData.CREATE_USER_URL, data=payload)
        assert response.status_code == 403
        assert response.json()['message'] == TestData.CREATE_USER_FIELD_ERROR
