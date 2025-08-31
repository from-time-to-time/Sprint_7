import requests
import allure

BASE_URL = "http://qa-scooter.praktikum-services.ru"

class ScooterApi:
    def __init__(self, base_url=BASE_URL, default_headers=None):
        self.base_url = base_url
        self.default_headers = default_headers or {}
    @allure.step('POST create courier')
    def create_courier(self, **kwargs):
        return requests.post(f"{BASE_URL}/api/v1/courier", **kwargs)

    @allure.step('POST login courier')
    def login_courier(self, **kwargs):
        return requests.post(f'{BASE_URL}/api/v1/courier/login', **kwargs)

    @allure.step('POST create order')
    def create_order(self, **kwargs):
        return requests.post(f'{BASE_URL}/api/v1/orders', **kwargs)

    @allure.step('GET list of orders')
    def get_orders(self, **kwargs):
        return requests.get(f'{BASE_URL}/api/v1/orders', **kwargs)

    @allure.step('DELETE courier')
    def delete_courier(self, courier_id: int, **kwargs):
        return requests.delete(f"{self.base_url}/api/v1/courier/{courier_id}", **kwargs)