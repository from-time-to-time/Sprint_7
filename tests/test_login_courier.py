import requests
import pytest
from src import config
import allure


class TestLoginCourier:
    @allure.title('Проверка авторизации зарегистрированного курьера')
    def test_login_existing_courier(self, register_new_courier_and_return_login_password):
        with allure.step('Получаем из фикстуры данные созданного курьера'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            login, password, first_name = register_new_courier_and_return_login_password
            body = {
                "login": login,
                "password": password,
                "firstName": first_name,
            }
        with allure.step('Отправляем POST-запрос со всеми полями зарегистрированного курьера'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = body, headers = config.headers)
        with allure.step('Проверяем, что получен статус 200 и id курьера'):
            assert response.status_code == 200
            assert response.json()['id']

    @allure.title('Проверка авторизации зарегистрированного курьера только с обязательными полями')
    def test_login_courier_with_required_fields(self, register_new_courier_and_return_login_password):
        with allure.step('Получаем из фикстуры логин и пароль созданного курьера (без firstName)'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            login, password, _ = register_new_courier_and_return_login_password
            body = {"login": login, "password": password}
        with allure.step('Отправляем POST-запрос только с обязательными полями зарегистрированного курьера'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = body, headers = config.headers)
        with allure.step('Проверяем, что вернулся статус 200 и id курьера'):
            assert response.status_code == 200
            assert response.json()['id']

    @allure.title('Проверка получения ошибки, если неправильно указать логин или пароль')
    @pytest.mark.parametrize("wrong_field", ["login", "password"])
    def test_login_courier_with_wrong_data(self, register_new_courier_and_return_login_password, wrong_field):
        with allure.step('Берем из фикстуры логин и пароль зарегистрированного курьера'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            login, password, _ = register_new_courier_and_return_login_password
            body = {"login": login, "password": password}
        with allure.step('Искажаем значение поля'):
            body[wrong_field] = body[wrong_field] + "123"
        with allure.step('Отправляем POST-запрос с некорректным значением в поле'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = body, headers = config.headers)
        with allure.step('Проверяем, что вернулась ошибка 404'):
            assert response.status_code == 404, f"{response.status_code}: {response.text}"
            message = response.json()['message']
            assert "Учетная запись не найдена" in message

    # присутствует баг в API, из-за этого авторизация курьера без пароля падает в 504 ошибку
    @allure.title('Проверка получения ошибки при авторизации курьера без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password"])
    def test_login_courier_without_one_of_required_fields(self, register_new_courier_and_return_login_password, missing_field):
        with allure.step('Берем из фикстуры логин и пароль зарегистрированного курьера'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            login, password, _ = register_new_courier_and_return_login_password
            body = {"login": login, "password": password}
        with allure.step('Удаляем одно из обязательных полей'):
            body.pop(missing_field)
        with allure.step('Отправляем POST-запрос без одного из обязательных полей'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = body, headers = config.headers)
        with allure.step('Проверяем, что вернулась ошибка со статусом 400'):
            assert response.status_code == 400, f"{response.status_code}: {response.text}"
            message = response.json()['message']
            assert "Недостаточно данных для входа" in message

    @allure.title('Проверка получения ошибки при авторизации незарегистрированного курьера')
    def test_login_nonexistent_courier(self, courier_payload_required):
        with allure.step('Отправляем POST-запрос с данными незарегистрированного курьера'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = courier_payload_required, headers = config.headers)
        with allure.step('Проверяем, что вернулась ошибка со статусом 404'):
            assert response.status_code == 404, f"{response.status_code}: {response.text}"
            message = response.json()['message']
            assert "Учетная запись не найдена" in message

    @allure.title('Проверка получения id при успешной авторизации')
    def test_get_id_after_login(self, register_new_courier_and_return_login_password):
        with allure.step('Получаем из фикстуры логин и пароль созданного курьера'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            login, password, _ = register_new_courier_and_return_login_password
            body = {
                "login": login,
                "password": password
            }
        with allure.step('Отправляем POST-запрос с логином и паролем'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier/login', json = body, headers = config.headers)
        with allure.step('Проверяем, что получен статус 200 и числовой id курьера'):
            assert response.status_code == 200
            assert response.json()['id']