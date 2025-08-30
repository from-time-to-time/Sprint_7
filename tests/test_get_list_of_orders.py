import requests
from src import config
import allure


class TestGetOrders:
    @allure.title('Проверка получения списка заказов')
    def test_get_list_of_orders(self):
        with allure.step('Отправляем GET-запрос для получения списка заказов'):
            response = requests.get(f'{config.BASE_URL}/api/v1/orders', headers = config.headers)
        with allure.step('Проверяем, что вернулся статус 200 и список не пустой'):
            assert response.status_code == 200
            orders = response.json().get("orders")
            assert len(orders) > 0, "Список заказов пуст"
