from src.scooter_api import ScooterApi
import allure


class TestGetOrders:
    @allure.title('Проверка получения списка заказов')
    def test_get_list_of_orders(self):
        api = ScooterApi()
        with allure.step('Отправляем GET-запрос для получения списка заказов'):
            response = api.get_orders()
        with allure.step('Проверяем, что вернулся статус 200 и список не пустой'):
            assert response.status_code == 200
            orders = response.json().get("orders")
            assert len(orders) > 0, "Список заказов пуст"
