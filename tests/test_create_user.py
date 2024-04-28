import pytest
import allure
from data import TestData
from conftest import user_model
from helpers import random_word, login_user, create_user


class TestCreateUser:

    @allure.title('Проверка создания пользователя c валидными значениями login, password, name')
    def test_create_user_with_valid_credentials(self, user_model):
        response_create = user_model['response_create']
        response_login = login_user(user_model['payload']['email'], user_model['payload']['password'])
        assert response_create.status_code == 200 and response_create.json()['success'] is True
        assert response_login.status_code == 200 and response_login.json()['success'] is True

    @allure.title('Проверка ошибки создания пользователя c занятыми login, password, name')
    def test_create_double_user_returns_error(self, user_model):
        response_second = create_user(user_model['payload']['email'],
                                      user_model['payload']['password'],
                                      user_model['payload']['name'])
        assert response_second.status_code == 403
        assert response_second.json()['message'] == TestData.CREATE_USER_EXIST_ERROR

    @allure.title('Проверка ошибки создания пользователя без одного из обязательных полей email, password, name')
    @pytest.mark.parametrize('email, password, name', [
        (random_word(), '', random_word()),
        (random_word(), None, random_word()),
        ('', random_word(), random_word()),
        (None, random_word(), random_word()),
        (random_word(), random_word(), ''),
        (random_word(), random_word(), None),
    ])
    def test_create_user_without_one_field_returns_error(self, email, password, name):
        response = create_user(email, password, name)
        assert response.status_code == 403
        assert response.json()['message'] == TestData.CREATE_USER_FIELD_ERROR
