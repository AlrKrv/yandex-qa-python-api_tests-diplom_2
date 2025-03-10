import pytest
import allure
import requests

from data.handlers import Urls, Handlers
from data.users_data import User


@allure.suite('Создание пользователя')
class TestCreateUser:

    @allure.description('Создание нового пользователя')
    @allure.title('Создание нового пользователя')
    def test_create_new_user_success(self):
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=User.create_data_user())
        assert response.status_code == 200 and response.json()["success"] is True

        response = requests.delete(f'{Urls.MAIN_URL}{Handlers.DELETE_USER}',
                                   headers={"Authorization": f'{response.json()["accessToken"]}'})
        assert response.status_code == 202 and response.json()["message"] == 'User successfully removed'

    @allure.description('При создании дублирующего пользователя срабатывает allert ')
    @allure.title('Создание пользователя который уже есть в системе')
    def test_create_double_user_error(self):
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=User.data_double)
        assert response.status_code == 403 and 'User already exists' in response.text

    @allure.description('При создании пользователя с некорректыми данными срабатывает allert')
    @allure.title('Создание пользователя с некорректными данными/ с незаполненными обязательными полями')
    @pytest.mark.parametrize("user_data", [User.data_without_email, User.data_without_password, User.data_without_name])
    def test_create_user_incorrect_data(self, user_data):
        response = requests.post(f'{Urls.MAIN_URL}{Handlers.CREATE_USER}', data=user_data)
        assert response.status_code == 403 and 'Email, password and name are required fields' in response.text
