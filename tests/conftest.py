import uuid
from datetime import datetime, timedelta

import pytest
import pytest_asyncio

from clerk import Client, types


@pytest_asyncio.fixture
async def client(httpserver):
    async with Client("foo", httpserver.url_for("")) as c:
        yield c


@pytest.fixture
def server_400_error():
    return types.Error(
        message="The provided cookie is invalid.",
        long_message="The provided cookie is invalid.",
        code="cookie_invalid",
        meta={},
    )


@pytest.fixture
def session_data(num_sessions):
    json_data = []
    sessions = []
    now = datetime.now()

    for _ in range(num_sessions):
        data = {
            "object": "session",
            "id": f"sess_{uuid.uuid4().hex}",
            "client_id": f"client_{uuid.uuid4().hex}",
            "user_id": f"user_{uuid.uuid4().hex}",
            "status": "active",
            "last_active_at": int(now.timestamp()),
            "expire_at": int((now + timedelta(days=7)).timestamp()),
            "abandon_at": int((now + timedelta(days=14)).timestamp()),
        }
        json_data.append(data)
        sessions.append(types.Session.model_validate(data))

    return json_data, sessions


@pytest.fixture
def users_data(faker, num_users):
    json_data = []
    users = []
    now = datetime.now()

    for _ in range(num_users):
        profile = faker.profile()
        email_id = f"idn_{uuid.uuid4().hex}"

        data = {
            "object": "user",
            "id": f"user_{uuid.uuid4().hex}",
            "username": profile["username"],
            "first_name": faker.first_name(),
            "last_name": faker.last_name(),
            "gender": profile["sex"],
            "birthday": "",
            "profile_image_url": faker.image_url(),
            "primary_email_address_id": email_id,
            "password_enabled": True,
            "two_factor_enabled": False,
            "created_at": int(now.timestamp()),
            "updated_at": int(now.timestamp()),
            "email_addresses": [
                {
                    "object": "email_address",
                    "id": email_id,
                    "email_address": profile["mail"],
                    "verification": {
                        "status": "verified",
                        "strategy": "",
                    },
                    "linked_to": [],
                }
            ],
            "phone_numbers": [],
            "external_accounts": [],
            "public_metadata": {},
            "unsafe_metadata": {},
            "private_metadata": {},
        }
        json_data.append(data)
        users.append(types.User.model_validate(data))

    return json_data, users


@pytest.fixture
def clients_data(num_clients):
    json_data = []
    clients = []

    for _ in range(num_clients):
        data = {
            "object": "client",
            "id": f"client_{uuid.uuid4().hex}",
            "last_active_session_id": f"sess_{uuid.uuid4().hex}",
            "sign_in_attempt_id": None,
            "sign_up_attempt_id": None,
            "ended": False,
        }
        json_data.append(data)
        clients.append(types.Client.model_validate(data))

    return json_data, clients
