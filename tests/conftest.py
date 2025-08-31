import random
import string
import pytest
import allure
from src.scooter_api import ScooterApi

# метод регистрации нового курьера возвращает список из логина и пароля
# если регистрация не удалась, возвращает пустой список
@pytest.fixture
def register_new_courier_and_return_login_password():
    # метод генерирует строку, состоящую только из букв нижнего регистра, в качестве параметра передаём длину строки
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for i in range(length))
        return random_string

    # создаём список, чтобы метод мог его вернуть
    login_pass = []

    # генерируем логин, пароль и имя курьера
    login = generate_random_string(10)
    password = generate_random_string(10)
    first_name = generate_random_string(10)

    # собираем тело запроса
    payload = {
        "login": login,
        "password": password,
        "firstName": first_name
    }

    # отправляем запрос на регистрацию курьера и сохраняем ответ в переменную response
    api = ScooterApi()
    response = api.create_courier(json=payload)

    # если регистрация прошла успешно (код ответа 201), добавляем в список логин и пароль курьера
    if response.status_code == 201:
        login_pass.append(login)
        login_pass.append(password)
        login_pass.append(first_name)

    # возвращаем список
    return login_pass

def _rnd(n=10) -> str:
    return ''.join(random.choice(string.ascii_lowercase) for _ in range(n))

@pytest.fixture
def courier_payload_required():
    return {"login": _rnd(), "password": _rnd()}

@pytest.fixture
def courier_payload_all():
    return {"login": _rnd(), "password": _rnd(), "firstName": _rnd()}

@pytest.fixture
def cleanup_courier_required(courier_payload_required):
    api = ScooterApi()
    yield
    creds = courier_payload_required
    with allure.step("Очищаем данные: логинимся и удаляем курьера"):
        try:
            auth = api.login_courier(json=creds)
            if auth.ok and "id" in auth.json():
                cid = auth.json()["id"]
                api.delete_courier(cid)
        except Exception as e:
            print(f"[cleanup] failed for {creds['login']}: {e}")

@pytest.fixture
def cleanup_courier_all(courier_payload_all):
    api = ScooterApi()
    yield
    creds = courier_payload_all
    with allure.step("Очищаем данные: логинимся и удаляем курьера"):
        try:
            auth = api.login_courier(creds)
            if auth.ok and "id" in auth.json():
                cid = auth.json()["id"]
                api.delete_courier(cid)
        except Exception as e:
            print(f"[cleanup all] failed for {creds['login']}: {e}")
