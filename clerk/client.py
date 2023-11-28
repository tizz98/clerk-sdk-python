import http
from contextlib import asynccontextmanager
from typing import Any, Mapping, Optional

import aiohttp

from clerk.errors import ClerkAPIException

__all__ = ["Client", "Service"]


class Client:
    """An API client for the clerk.dev API"""

    def __init__(
        self, token: str, base_url: str = "https://api.clerk.dev/v1/", timeout_seconds: float = 30.0
    ) -> None:
        self._session = aiohttp.ClientSession(
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=aiohttp.ClientTimeout(total=timeout_seconds),
        )
        self._base_url = base_url

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self._session.close()

    @property
    def verification(self):
        from clerk.verification import VerificationService

        return VerificationService(self)

    @property
    def session(self):
        from clerk.sessions import SessionsService

        return SessionsService(self)

    @property
    def clients(self):
        from clerk.clients import ClientsService

        return ClientsService(self)

    @property
    def users(self):
        from clerk.users import UsersService

        return UsersService(self)

    @property
    def organizations(self):
        from clerk.organizations import OrganizationsService

        return OrganizationsService(self)

    @asynccontextmanager
    async def get(
        self, endpoint: str, params: Optional[Mapping[str, str]] = None
    ) -> aiohttp.ClientResponse:
        async with self._session.get(self._make_url(endpoint), params=params) as r:
            await self._check_response_err(r)
            yield r

    @asynccontextmanager
    async def post(
        self, endpoint: str, data: Any = None, json: Any = None
    ) -> aiohttp.ClientResponse:
        async with self._session.post(self._make_url(endpoint), data=data, json=json) as r:
            await self._check_response_err(r)
            yield r

    @asynccontextmanager
    async def delete(self, endpoint: str) -> aiohttp.ClientResponse:
        async with self._session.delete(self._make_url(endpoint)) as r:
            await self._check_response_err(r)
            yield r

    @asynccontextmanager
    async def patch(
        self, endpoint: str, data: Any = None, json: Any = None
    ) -> aiohttp.ClientResponse:
        async with self._session.patch(self._make_url(endpoint), data=data, json=json) as r:
            await self._check_response_err(r)
            yield r

    async def _check_response_err(self, r: aiohttp.ClientResponse):
        if http.HTTPStatus.OK <= r.status < http.HTTPStatus.BAD_REQUEST:
            return  # no error
        raise await ClerkAPIException.from_response(r)

    def _make_url(self, endpoint: str) -> str:
        return f"{self._base_url.rstrip('/')}/{endpoint.strip('/')}/"


class Service:
    """Base Clerk service"""

    def __init__(self, client: Client) -> None:
        self._client = client
