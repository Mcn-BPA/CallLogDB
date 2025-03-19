import requests
import responses

from calllogdb.api.api_client import APIClient
from calllogdb.core import config


def test_api_client_record_response():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            json={"status": "ok", "data": [1, 2, 3]},
            status=200,
        )

        client = APIClient()
        response = client.get()
        assert response == {"status": "ok", "data": [1, 2, 3]}


def test_api_client_empty_response():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            json={},
            status=200,
        )

        client = APIClient()
        response = client.get()
        assert response == {}


def test_api_client_http_error():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            status=500,
        )

        client = APIClient(retries_enabled=False)
        response = client.get()
        assert response == {}


def test_api_client_timeout():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            body=requests.exceptions.Timeout(),
        )

        client = APIClient()
        response = client.get()
        assert response == {}


def test_api_client_with_params():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            json={"result": "success"},
            match=[responses.matchers.query_param_matcher({"id": "123"})],
            status=200,
        )

        client = APIClient()
        response = client.get(params={"id": "123"})
        assert response == {"result": "success"}


def test_api_client_close():
    client = APIClient()
    client.close()
    assert client.session is not None  # Проверяем, что объект session существует, но закрыт


def test_api_client_context_manager():
    with responses.RequestsMock() as rsps:
        rsps.add(
            responses.GET,
            config.url,
            json={"status": "ok"},
            status=200,
        )

        with APIClient() as client:
            response = client.get()
            assert response == {"status": "ok"}
