import pytest
import allure
from data import TestData
from helpers import random_word, create_user, delete_user, edit_user


class TestEditUser:
    access_token = None

    def setup_method(self):
        self.email = random_word()
        self.password = random_word()
        self.name = random_word()
        response_create = create_user(self.email, self.password, self.name)
        self.access_token = response_create.json()['accessToken']

    def teardown_method(self):
        delete_user(self.access_token)

    @pytest.mark.parametrize('field, payload', [
        ('email', {'email': random_word() + '@ya.ru'}),
        ('name', {'name': random_word()})
    ])
    @allure.title('Проверка редактирования пользователя с авторизацией')
    def test_edit_user_with_authorization(self, field, payload):
        response_edit = edit_user(payload, self.access_token)
        assert response_edit.status_code == 200
        assert response_edit.json()['user'][field] == payload[field]

    @pytest.mark.parametrize('payload', [
        {'email': random_word() + '@ya.ru'},
        {'name': random_word()}
    ])
    @allure.title('Проверка редактирования пользователя без авторизации')
    def test_edit_user_without_authorization(self, payload):
        response_edit = edit_user(payload, None)
        assert response_edit.status_code == 401
        assert response_edit.json()['message'] == TestData.AUTH_ERROR
