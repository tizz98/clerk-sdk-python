import pytest

from clerk import errors


@pytest.mark.asyncio
class TestVerify:
    @pytest.mark.parametrize("num_sessions", [1])
    async def test_verify_with_session_id(self, client, httpserver, session_data):
        expected_session = session_data[1][0]
        session_json = session_data[0][0]
        httpserver.expect_request(
            f"/sessions/{expected_session.id}/verify/", "POST", json={"token": "some-token"}
        ).respond_with_json(session_json)

        session = await client.verification.verify("some-token", expected_session.id)
        assert session == expected_session

    @pytest.mark.parametrize("num_sessions", [1])
    @pytest.mark.parametrize("num_clients", [1])
    async def test_verify_without_session_id_and_active_session(
        self, client, httpserver, session_data, clients_data
    ):
        expected_session = session_data[1][0]
        session_json = session_data[0][0]
        clients_json = clients_data[0][0]
        clients_json["id"] = expected_session.client_id
        clients_json["last_active_session_id"] = expected_session.id

        httpserver.expect_request(
            "/clients/verify/", "POST", json={"token": "some-token"}
        ).respond_with_json(clients_json)
        httpserver.expect_request(f"/sessions/{expected_session.id}/", "GET").respond_with_json(
            session_json
        )

        session = await client.verification.verify("some-token")
        assert session == expected_session

    @pytest.mark.parametrize("num_clients", [1])
    async def test_verify_without_session_id_and_no_active_session(
        self, client, httpserver, clients_data
    ):
        clients_json = clients_data[0][0]
        clients_json["last_active_session_id"] = None

        httpserver.expect_request(
            "/clients/verify/", "POST", json={"token": "some-token"}
        ).respond_with_json(clients_json)

        with pytest.raises(errors.NoActiveSessionException):
            await client.verification.verify("some-token")
