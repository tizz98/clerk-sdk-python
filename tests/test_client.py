import pytest

from clerk import errors, types


class TestAPIErrorHandling:
    def _check_error(self, e: errors.ClerkAPIException, err):
        assert e.status_code == 400
        assert e.data is not None
        assert e.url is not None
        assert e.api_errors == (err,)

    @pytest.mark.asyncio
    async def test_sessions_service_handles_errors(self, client, httpserver, server_400_error):
        httpserver.expect_request("/sessions/", "GET").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/sessions/123/", "GET").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/sessions/123/revoke/", "POST").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/sessions/123/verify/", "POST").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.session.list()

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.session.get("123")

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.session.revoke("123")

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.session.verify("123", "x")

        self._check_error(e.value, server_400_error)

    @pytest.mark.asyncio
    async def test_users_service_handles_errors(self, client, httpserver, server_400_error):
        httpserver.expect_request("/users/", "GET").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/users/123/").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.users.list()

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.users.get("123")

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.users.delete("123")

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.users.update("123", types.UpdateUserRequest())

        self._check_error(e.value, server_400_error)

    @pytest.mark.asyncio
    async def test_clients_service_handles_errors(self, client, httpserver, server_400_error):
        httpserver.expect_request("/clients/", "GET").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/clients/123/", "GET").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )
        httpserver.expect_request("/clients/verify/", "POST").respond_with_json(
            {"errors": [server_400_error.model_dump()]}, status=400
        )

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.clients.list()

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.clients.get("123")

        self._check_error(e.value, server_400_error)

        with pytest.raises(errors.ClerkAPIException) as e:
            await client.clients.verify("token")

        self._check_error(e.value, server_400_error)
