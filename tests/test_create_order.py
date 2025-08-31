import pytest
from src.scooter_api import ScooterApi
import allure


BASE_ORDER = {
    "firstName": "Naruto",
    "lastName": "Uchiha",
    "address": "Konoha, 142 apt.",
    "metroStation": 4,
    "phone": "+7 800 355 35 35",
    "rentTime": 5,
    "deliveryDate": "2020-06-06",
    "comment": "Saske, come back to Konoha"
    }
class TestCreateOrder:
        @allure.title('Проверка создания заказа')
        @pytest.mark.parametrize(
            "color_data",
            [
                {"color": ["BLACK"]},
                {"color": ["GREY"]},
                {"color": ["BLACK", "GREY"]},
                {"color": []},
                {},
            ],
            ids=["only_black", "only_grey", "both", "empty", "missing"]
        )
        def test_create_order_with_different_color_data(self, color_data):
            api = ScooterApi()
            with allure.step('Готовим payload'):
                body = {**BASE_ORDER, **color_data}

            with allure.step('Отправляем POST-запрос на создание заказа с одним из вариантов color'):
                response = api.create_order(json=body)

            with allure.step('Проверяем, что вернулся статус 201 и трек-номер'):
                assert response.status_code == 201, f"{response.status_code}: {response.text}"
                assert response.json().get('track')