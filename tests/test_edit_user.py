import pytest
import allure
from data import TestData
from helpers import random_word, edit_user
from conftest import user_model


class TestEditUser:

    @pytest.mark.parametrize('field, payload', [
        ('email', {'email': random_word() + '@ya.ru'}),
        ('name', {'name': random_word()})
    ])
    @allure.title('Проверка редактирования пользователя с авторизацией')
    def test_edit_user_with_authorization(self, field, payload, user_model):
        response_edit = edit_user(payload, user_model['response_create'].json()['accessToken'])
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
