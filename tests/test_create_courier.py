import requests
import pytest
from src import config
import allure


class TestCreateCourier:
    @allure.title('Проверка создания нового курьера')
    def test_create_new_courier(self, courier_payload_all, cleanup_courier_all):
        with allure.step("Отправляем запрос на создание курьера со всеми полями незарегистрированного курьера из фикстуры"):
            resp = requests.post(f"{config.BASE_URL}/api/v1/courier", json=courier_payload_all, headers=config.headers)

        with allure.step("Проверяем, что курьер успешно создан: есть статус-код и тело ответа"):
            assert resp.status_code == 201, f"Ожидали 201, получили {resp.status_code}: {resp.text}"
            body = resp.json()
            assert body.get("ok") is True, f"Ожидали ok=true, получили: {body}"


    @allure.title('Проверка невозможности создания двух одинаковых курьеров')
    def test_cant_create_existing_courier(self, register_new_courier_and_return_login_password):
        with allure.step('Создаем курьера и берем его данные'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            existing_login, existing_password, existing_firstname = register_new_courier_and_return_login_password

        with allure.step('Готовим тело запроса для создания с теми же полями'):
            body = {
                "login": existing_login,
                "password": existing_password,
                "firstName": existing_firstname,
            }
        with allure.step('Отправляем POST-запрос с теми же данными, что и у ранее созданного курьера'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json = body, headers = config.headers)

        with allure.step('Проверяем, что в ответе получили ошибку 409'):
            assert response.status_code == 409
            message = response.json()['message']
            assert 'Этот логин уже используется' in message


    @allure.title('Проверка создания нового курьера при отправке всех обязательных полей')
    def test_create_courier_with_required_fields(self, courier_payload_required, cleanup_courier_required):
        with allure.step('Формируем тело запроса только с обязательными полями (login, password)'):
            body = {"login": courier_payload_required["login"], "password": courier_payload_required["password"]}

        with allure.step('Отправляем POST-запрос только с обязательными полями'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json=body, headers=config.headers)

        with allure.step('Проверяем, что курьер успешно создан: есть статус-код и тело ответа"'):
            assert response.status_code == 201, f"{response.status_code}: {response.text}"
            payload = response.json()
            assert payload.get('ok') is True, f"Ожидали ok=true, получили: {payload}"


    @allure.title('Проверка получения кода ответа 201 при создании курьера')
    def test_create_new_courier_return_code_201(self, courier_payload_all, cleanup_courier_all):
        with allure.step("Отправляем запрос на создание со всеми полями незарегистрированного курьера из фикстуры"):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json=courier_payload_all, headers=config.headers)

        with allure.step('Проверяем, что в ответ получили код 201'):
            assert response.status_code == 201, f"Ожидали 201, получили {response.status_code}, {response.text}"

    @allure.title('Проверка получения ok:true при создании курьера+')
    def test_create_new_courier_return_ok(self, courier_payload_all, cleanup_courier_all):
        with allure.step("Отправляем запрос на создание со всеми полями незарегистрированного курьера из фикстуры"):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json=courier_payload_all, headers=config.headers)

        with allure.step('Проверяем, что в ответ получили "ok"'):
            assert response.json()['ok'] == True, f"Ожидали 'ok', получили {response.text}"


    @allure.title('Проверка получения ошибки при создании курьера без одного из обязательных полей')
    @pytest.mark.parametrize("missing_field", ["login", "password"], ids=["no_login", "no_password"])
    def test_create_courier_with_missing_required_field(self, courier_payload_required, missing_field, cleanup_courier_required):
        with allure.step('Берем поля незарегистрированного курьера из фикстуры и копируем для безопасного изменения'):
            body = courier_payload_required.copy()

        with allure.step('Удаляем одно из обязательных полей'):
            body.pop(missing_field)

        with allure.step('Отправляем POST-запрос только с одним обязательным полем'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json=body, headers=config.headers)

        with allure.step('Проверяем, что в ответ получена ошибка 400'):
            assert response.status_code == 400, f"{response.status_code}: {response.text}"
            message = response.json().get('message', '')
            assert "Недостаточно данных для создания учетной записи" in message


    @allure.title('Проверка получения ошибки при создании нового курьера с уже существующим логином')
    def test_create_user_with_existing_login(self, courier_payload_all, register_new_courier_and_return_login_password, cleanup_courier_all):
        with allure.step('Создаем курьера и берем его login как уже существующий'):
            assert register_new_courier_and_return_login_password, "Фикстура не создала курьера"
            existing_login, _, _ = register_new_courier_and_return_login_password

        with allure.step('Готовим тело запроса: используем payload из фикстуры, но подставляем существующий login'):
            body = courier_payload_all.copy()
            body["login"] = existing_login

        with allure.step('Отправляем POST-запрос с уже существующим login'):
            response = requests.post(f'{config.BASE_URL}/api/v1/courier', json=body, headers=config.headers)

        with allure.step('Проверяем, что в ответ получена ошибка 409'):
            assert response.status_code == 409, f"{response.status_code}: {response.text}"
            payload = response.json()
            assert 'message' in payload and 'Этот логин уже используется' in payload['message']
