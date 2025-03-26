import allure
import jsonschema
import requests
from .schemas.pet_schema import PET_SCHEMA

BASE_URL = "http://5.181.109.28:9090/api/v3"

@allure.feature("Pet")
class TestPet:
    @allure.title("Попытка удалить несуществующего питомца")
    def test_delete_nonexistent_pet(self):
        with allure.step("Отправка запроса на удаление несуществующего питомца"):
            response = requests.delete(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 200, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet deleted", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка обновить несуществующего питомца")
    def test_update_nonexistent_pet(self):
        with allure.step("Отправка запроса на обновление несуществующего питомца"):
            payload = {
                "id": 9999,
                "name": "Non-existent Pet",
                "status": "available"
            }
            response = requests.put(url=f"{BASE_URL}/pet", json=payload)

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

        with allure.step("Проверка текстового содержимого ответа"):
            assert response.text == "Pet not found", "Текст ошибки не совпал с ожидаемым"

    @allure.title("Попытка получить информацию о несуществующем питомце")
    def test_get_info_nonexistent_pet(self):
        with allure.step("Отправка запроса на получение информации о несуществующем питомце"):
            response = requests.get(url=f"{BASE_URL}/pet/9999")

        with allure.step("Проверка статуса ответа"):
            assert response.status_code == 404, "Код ответа не совпал с ожидаемым"

    @allure.title("Добавление нового питомца")
    def test_add_pet(self):
        with allure.step("Подготовка данных для создания питомца"):
            payload = {
                "id": 1,
                "name": "Buddy",
                "status": "available"
            }
        with allure.step("Отправка запроса на создание питомца"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка папаметров питомца в ответе"):
            assert response_json['id'] == payload['id'], "id питомца не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца не совпадает с ожидаемым"

    @allure.title("Добавление нового питомца c полными данными")
    def test_add_full_data_pet(self):
        with allure.step("Подготовка данных для создания питомца с полными данными"):
            payload = {
                "id": 10,
                "name": "doggie",
                "category": {"id": 1, "name": "Dogs"},
                "photoUrls": ["string"],
                "tags": [{"id": 0, "name": "string"}],
                "status": "available"
            }

        with allure.step("Отправка запроса на создание питомца с полными данными"):
            response = requests.post(url=f"{BASE_URL}/pet", json=payload)
            response_json = response.json()

        with allure.step("Проверка статуса ответа и валидация JSON-схемы"):
            assert response.status_code == 200
            jsonschema.validate(response.json(), PET_SCHEMA)

        with allure.step("Проверка папаметров питомца с полными данными в ответе"):
            assert response_json['id'] == payload['id'], "id питомца с полными данными не совпадает с ожидаемым"
            assert response_json['name'] == payload['name'], "Имя питомца с полными данными не совпадает с ожидаемым"
            assert response_json['category'] == payload['category'], "Категория питомца с полными данными не совпадает с ожидаемым"
            assert response_json['photoUrls'] == payload['photoUrls'], "Ссылка на питомца с полными данными не совпадает с ожидаемым"
            assert response_json['tags'] == payload['tags'], "Тэги питомца с полными данными не совпадает с ожидаемым"
            assert response_json['status'] == payload['status'], "Статус питомца с полными данными не совпадает с ожидаемым"

    @allure.title("Получение информации о питомце по ID")
    def test_get_pet_by_id(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Отправка запроса на получение информации о питомце по ID"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")

        with allure.step("Проверка статуса ответа и данных питомца"):
            assert response.status_code == 200
            assert response.json()["id"] == pet_id

    @allure.title("Обновление информации о питомце")
    def test_put_update_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Проверка статуса ответа созданного питомца"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Ошибка при создании питомца"

        with allure.step("Отправка PUT-запроса на обновление питомца"):
            updated_pet_data = {"id": pet_id, "name": "Buddy Updated", "status": "sold"}
            response = requests.put(f"{BASE_URL}/pet", json=updated_pet_data)
            assert response.status_code == 200, "Ошибка при обновлении питомца"

        with allure.step("Проверка папаметров обновленного питомца с полными данными в ответе"):
            updated_pet = response.json()
            assert updated_pet['id'] == pet_id, "id питомца не совпадает с ожидаемым"
            assert updated_pet['name'] == "Buddy Updated", "Имя питомца не совпадает с ожидаемым"
            assert updated_pet['status'] == "sold", "Статус питомца не обновлен"

    @allure.title("Удаление питомца по ID")
    def test_delete_pet(self, create_pet):
        with allure.step("Получение ID созданного питомца"):
            pet_id = create_pet["id"]

        with allure.step("Проверка статуса ответа созданного питомца"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Ошибка при создании питомца"

        with allure.step("Отправка DELETE-запроса на удаление питомца"):
            response = requests.delete(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 200, "Ошибка при удалении питомца"

        with allure.step("Отправка GET-запроса для проверки, что питомец был удален"):
            response = requests.get(f"{BASE_URL}/pet/{pet_id}")
            assert response.status_code == 404, "Питомец не был удален, статус должен быть 404"

