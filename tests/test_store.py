import allure
import jsonschema
import pytest
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("PetStore")
class TestPetStore:
    @allure.title("Размещение заказа")
    def test_add_pet_order(self):
        with allure.step("Подготовка данных для заказа питомца"):
            order_data = {
                "id": 1,
                "petId": 1,
                "quantity": 1,
                "status": "placed",
                "complete": True
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/store/order", json=order_data)
            response_json = response.json()

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200

        with allure.step("Проверка папаметров питомца в ответе"):
            assert response_json['id'] == order_data['id'], "id заказа не совпадает с ожидаемым"
            assert response_json['petId'] == order_data['petId'], "Id питомца не совпадает с ожидаемым"
            assert response_json['quantity'] == order_data['quantity'], "Количество питомцев не совпадает с ожидаемым"
            assert response_json['status'] == order_data['status'], "Статус заказа не совпадает с ожидаемым"
            assert response_json['complete'] == order_data['complete'], "Статус завершенности заказа не совпадает с ожидаемым"

    @allure.title("Получение информации о заказе по ID")
    def test_get_info_about_order_by_id(self):
        with allure.step("Отправка GET-запроса"):
            order_id = 1
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        with allure.step("Проверка, что ответ содержит данные заказа с id = 1"):
            response_json = response.json()
            assert response_json['id'] == order_id, f"Expected order id {order_id}, but got {response_json['id']}"

    @allure.title("Удаление заказа по ID")
    def test_delete_order(self):
        with allure.step("Отправка DELETE-запроса"):
            order_id = 1
            delete_response = requests.delete(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка статуса ответа об удалении"):
            assert delete_response.status_code == 200, f"Unexpected status code on DELETE: {delete_response.status_code}"

        with allure.step("Проверка, что заказ больше не существует"):
            get_response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка, что статус-код ответа 404 по запросу на удаленный заказ"):
            assert get_response.status_code == 404, f"Unexpected status code on GET after DELETE: {get_response.status_code}"

    @allure.title("Попытка получить информацию о несуществующем заказе")
    def test_get_nonexistent_order(self):
        with allure.step("Отправка GET-запроса"):
            order_id = 9999
            response = requests.get(f"{BASE_URL}/store/order/{order_id}")

        with allure.step("Проверка, что статус-код ответа 404"):
            assert response.status_code == 404, f"Unexpected status code: {response.status_code}"

    @allure.title("Получение инвентаря магазина")
    def test_get_inventory(self):
        with allure.step("Тестовый случай для проверки GET-запроса на инвентарь"):
            response = requests.get(f"{BASE_URL}/store/inventory")

        with allure.step("Проверка, что статус-код ответа  200"):
            assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        with allure.step("Проверка, что ответ содержит данные инвентаря в нужном формате"):
            expected_data = {"approved": 57, "delivered": 50}
            assert response.json() == expected_data, f"Unexpected response data: {response.json()}"

