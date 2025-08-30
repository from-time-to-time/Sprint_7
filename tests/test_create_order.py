import requests
import pytest
from src import config
import allure


class TestCreateOrder:
    @allure.title('Проверка создания заказа')
    @pytest.mark.parametrize("color",
                             [
                                 ["BLACK"],
                                 ["GREY"],
                                 ["BLACK", "GREY"],
                                 [],
                                 None
                             ],
                             ids=["only_black", "only_grey", "both", "empty", "missing"])
    def test_create_order_with_different_color_data(self, color):
        payload = {
                "firstName": "Naruto",
                "lastName": "Uchiha",
                "address": "Konoha, 142 apt.",
                "metroStation": 4,
                "phone": "+7 800 355 35 35",
                "rentTime": 5,
                "deliveryDate": "2020-06-06",
                "comment": "Saske, come back to Konoha",
                "color": []
        }
        with allure.step('Готовим базовый payload для создания заказа'):
            body = payload.copy()
        with allure.step('Меняем значение поля color'):
            if color is None:
                body.pop('color')
            else:
                body["color"] = color
        with allure.step('Отправляем POST-запрос с одним из вариантов color'):
            response = requests.post(f'{config.BASE_URL}/api/v1/orders', json = body, headers = config.headers)
        with allure.step('Проверяем, что вернулся статус 201 и трек-номер'):
            assert response.status_code == 201, f"{response.status_code}: {response.text}"
            assert response.json()['track']