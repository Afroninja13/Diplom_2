import random
import string
import allure
import requests
from data import TestData


@allure.step('Создаем рандомное слово из 6 символов')
def random_word():
    return str(''.join(random.choice(string.ascii_letters) for x in range(6))).lower()


@allure.step('Создаем пользователя')
def create_user(email=None, password=None, name=None):
    payload = {'email': email, 'password': password, 'name': name}
    response_create = requests.post(TestData.BASE_URL + TestData.CREATE_USER_URL, data=payload)
    return response_create


@allure.step('Логинимся пользователем')
def login_user(email=None, password=None):
    payload = {'email': email, 'password': password}
    response_login = requests.post(TestData.BASE_URL + TestData.LOGIN_USER_URL, data=payload)
    return response_login


@allure.step('Удаляем пользователем')
def delete_user(access_token):
    headers = {'Authorization': access_token}
    response_delete = requests.delete(TestData.BASE_URL + TestData.BASE_USER_URL, headers=headers)
    return response_delete


@allure.step('Изменяем данные пользователя')
def edit_user(payload, access_token):
    headers = {'Authorization': access_token}
    response_edit = requests.patch(TestData.BASE_URL + TestData.BASE_USER_URL, headers=headers, data=payload)
    return response_edit


@allure.step('Изменяем данные пользователя')
def create_order(ingredients, access_token):
    headers = {'Authorization': access_token}
    payload = {'ingredients': ingredients}
    response_create = requests.post(TestData.BASE_URL + TestData.ORDER_URL, headers=headers, data=payload)
    return response_create


@allure.step('Получаем данные о всех ингредиентах')
def get_ingredients_data():
    response_ingredients_list = requests.get(TestData.BASE_URL + TestData.INGREDIENTS_URL)
    return response_ingredients_list


@allure.step('Получаем заказы конкретного пользователя')
def get_user_orders(access_token):
    headers = {'Authorization': access_token}
    response_orders = requests.get(TestData.BASE_URL + TestData.ORDER_URL, headers=headers)
    return response_orders
