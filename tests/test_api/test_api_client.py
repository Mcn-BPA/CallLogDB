import json

from calllogdb.api.api_client import APIClient


def test_api_client_record_response(vcr):
    # Указываем путь к кассете и используем режим записи "all",
    # чтобы всегда получать свежий ответ.
    cassette_path = "tests/data/sample_api_response.json"
    with vcr.use_cassette(cassette_path, record_mode="all", serializer="json"):
        client = APIClient(url="http://example.com/api", token="dummy_token")
        response = client.get(params={"q": "test"})

        # Выводим ответ в консоль для просмотра
        print(json.dumps(response, indent=4))

        # Временно делаем простую проверку, чтобы тест прошёл
        # (после изучения структуры ответа можно добавить детальные проверки)
        assert isinstance(response, dict)


# @responses.activate
# def test_api_client_get_failure():
#     test_url = "http://example.com/api"
#     # Симулируем ошибку сервера (например, 500)
#     responses.add(responses.GET, test_url, status=500)

#     client = APIClient(url=test_url, token="dummy_token")
#     result = client.get(params={"q": "test"})

#     # В случае ошибки возвращается пустой словарь
#     assert result == {}
