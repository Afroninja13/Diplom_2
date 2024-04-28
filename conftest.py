import requests
import pytest
from helpers import random_word, get_ingredients_data
from data import TestData


@pytest.fixture(scope='function')
def user_model():
    """
    Создает юзера с рандомными email, password, name.
    Возвращает в вызывающую функцию response создания и словарь с email, password, name.
    Удаляет созданного юзера.
    """
    payload = {'email': random_word() + "@ya.ru", 'password': random_word(), 'name': random_word()}
    response_create = requests.post(TestData.BASE_URL + TestData.CREATE_USER_URL, data=payload)
    access_token = response_create.json()['accessToken']
    yield {'response_create': response_create, 'payload': payload}
    headers = {'Authorization': access_token}
    requests.delete(TestData.BASE_URL + TestData.BASE_USER_URL, headers=headers)


@pytest.fixture(scope='function')
def order_model():
    """
    Получает json дату всех ингредиентов.
    Создает список с хешем одного ингредиента.
    Возвращает в вызывающую функцию список с одним ингредиентом.
    """
    ingredients_data = get_ingredients_data().json()
    ingredients_id_list = [ingredients_data['data'][0]['_id']]
    yield {'ingredients_id_list': ingredients_id_list}
