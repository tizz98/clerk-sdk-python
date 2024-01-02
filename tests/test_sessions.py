import pytest


class TestList:
    @pytest.mark.parametrize("num_sessions", [0, 1, 2])
    @pytest.mark.asyncio
    async def test_valid_data_is_parsed_properly(self, client, httpserver, session_data):
        httpserver.expect_request("/sessions/", "GET").respond_with_json(session_data[0])
        sessions = await client.session.list()
        assert sessions == session_data[1]


class TestGet:
    @pytest.mark.parametrize("num_sessions", [1])
    @pytest.mark.asyncio
    async def test_valid_data_is_parsed_properly(self, client, httpserver, session_data):
        expected_session = session_data[1][0]
        session_json = session_data[0][0]
        httpserver.expect_request(f"/sessions/{expected_session.id}/", "GET").respond_with_json(
            session_json
        )

        session = await client.session.get(expected_session.id)
        assert session == expected_session


class TestRevoke:
    @pytest.mark.parametrize("num_sessions", [1])
    @pytest.mark.asyncio
    async def test_valid_request_returns_revoked_session(self, client, httpserver, session_data):
        expected_session = session_data[1][0]
        session_json = session_data[0][0]
        httpserver.expect_request(
            f"/sessions/{expected_session.id}/revoke/", "POST"
        ).respond_with_json(session_json)

        session = await client.session.revoke(expected_session.id)
        assert session == expected_session


class TestVerify:
    @pytest.mark.parametrize("num_sessions", [1])
    @pytest.mark.asyncio
    async def test_valid_request_returns_verified_session(self, client, httpserver, session_data):
        expected_session = session_data[1][0]
        session_json = session_data[0][0]
        httpserver.expect_request(
            f"/sessions/{expected_session.id}/verify/", "POST", json={"token": "some-token"}
        ).respond_with_json(session_json)

        session = await client.session.verify(expected_session.id, "some-token")
        assert session == expected_session
