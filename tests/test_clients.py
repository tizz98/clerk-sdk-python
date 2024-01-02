import pytest


class TestList:
    @pytest.mark.parametrize("num_clients", [0, 1, 2])
    @pytest.mark.asyncio
    async def test_valid_data_is_parsed_properly(self, client, httpserver, clients_data):
        httpserver.expect_request("/clients/", "GET").respond_with_json(clients_data[0])
        clients = await client.clients.list()
        assert clients == clients_data[1]


class TestGet:
    @pytest.mark.parametrize("num_clients", [1])
    @pytest.mark.asyncio
    async def test_valid_data_is_parsed_properly(self, client, httpserver, clients_data):
        expected_client = clients_data[1][0]
        clients_json = clients_data[0][0]

        httpserver.expect_request(f"/clients/{expected_client.id}/", "GET").respond_with_json(
            clients_json
        )
        client = await client.clients.get(expected_client.id)
        assert client == expected_client


class TestVerify:
    @pytest.mark.parametrize("num_clients", [1])
    @pytest.mark.asyncio
    async def test_valid_data_is_parsed_properly(self, client, httpserver, clients_data):
        expected_client = clients_data[1][0]
        clients_json = clients_data[0][0]

        httpserver.expect_request(
            "/clients/verify/", "POST", json={"token": "123"}
        ).respond_with_json(clients_json)
        client = await client.clients.verify("123")
        assert client == expected_client
