import uuid

import pytest

from clerk import types


@pytest.mark.asyncio
class TestList:
    @pytest.mark.parametrize("num_users", [0, 1, 2])
    async def test_valid_data_is_parsed_properly(self, client, httpserver, users_data):
        httpserver.expect_request("/users/", "GET").respond_with_json(users_data[0])
        users = await client.users.list()
        assert users == users_data[1]


@pytest.mark.asyncio
class TestGet:
    @pytest.mark.parametrize("num_users", [1])
    async def test_valid_data_is_parsed_properly(self, client, httpserver, users_data):
        user_json = users_data[0][0]
        expected_user = users_data[1][0]

        httpserver.expect_request(f"/users/{expected_user.id}/", "GET").respond_with_json(user_json)
        got_user = await client.users.get(expected_user.id)
        assert got_user == expected_user


@pytest.mark.asyncio
class TestDelete:
    async def test_valid_data_is_parsed_properly(self, client, httpserver):
        user_id = f"user_{uuid.uuid4().hex}"
        httpserver.expect_request(f"/users/{user_id}/", "DELETE").respond_with_json(
            {"object": "user", "id": user_id, "deleted": True}
        )
        resp = await client.users.delete(user_id)
        assert resp == types.DeleteUserResponse(
            object="user",
            id=user_id,
            deleted=True,
        )


@pytest.mark.asyncio
class TestUpdate:
    @pytest.mark.parametrize("num_users", [1])
    @pytest.mark.parametrize(
        "req,expected_req_json",
        [
            (types.UpdateUserRequest(), {}),
            (types.UpdateUserRequest(first_name="Bob"), {"first_name": "Bob"}),
            (
                types.UpdateUserRequest(
                    first_name="Bob",
                    last_name="Jones",
                    primary_email_address_id="idn_123",
                    profile_image="https://example.com",
                    password="123",
                ),
                {
                    "first_name": "Bob",
                    "last_name": "Jones",
                    "primary_email_address_id": "idn_123",
                    "profile_image": "https://example.com",
                    "password": "123",
                },
            ),
        ],
    )
    async def test_valid_data_is_parsed_properly(
        self, client, httpserver, users_data, req, expected_req_json
    ):
        user_json = users_data[0][0]
        expected_user = users_data[1][0]

        httpserver.expect_request(
            f"/users/{expected_user.id}/", "PATCH", json=expected_req_json
        ).respond_with_json(user_json)

        got_user = await client.users.update(expected_user.id, req)
        assert got_user == expected_user
