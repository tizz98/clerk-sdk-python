from typing import Any, Mapping
import http

from pydantic import BaseModel
import httpx

from clerk.errors import ClerkAPIException

__all__ = ["Client", "Service"]


class Client:
    """An API client for the clerk.dev API"""

    def __init__(
        self, token: str, base_url: str = "https://api.clerk.dev/v1/", timeout_seconds: float = 30.0
    ) -> None:
        self._session = httpx.AsyncClient(
            headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
            timeout=httpx.Timeout(timeout_seconds),
        )
        self._base_url = base_url

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

    async def get(self, endpoint: str, params: Mapping[str, str] | None = None) -> httpx.Response:
        r = await self._session.get(self._make_url(endpoint), params=params)
        await self._check_response_err(r)
        return r

    async def post(
        self, endpoint: str, request: BaseModel | None = None, json: Any = None
    ) -> httpx.Response:
        r = await self._session.post(
            self._make_url(endpoint),
            data=request.model_dump_json() if request else None,
            json=json,
        )
        await self._check_response_err(r)
        return r

    async def delete(self, endpoint: str) -> httpx.Response:
        r = await self._session.delete(self._make_url(endpoint))
        await self._check_response_err(r)
        return r

    async def patch(
        self, endpoint: str, request: BaseModel | None = None, json: Any = None
    ) -> httpx.Response:
        r = await self._session.patch(
            self._make_url(endpoint), data=request and request.model_dump_json(), json=json
        )
        await self._check_response_err(r)
        return r

    async def _check_response_err(self, r: httpx.Response):
        if not http.HTTPStatus.OK <= r.status_code < http.HTTPStatus.BAD_REQUEST:
            raise await ClerkAPIException.from_response(r)

    def _make_url(self, endpoint: str) -> str:
        return f"{self._base_url.rstrip('/')}/{endpoint.strip('/')}/"


class Service:
    """Base Clerk service"""

    def __init__(self, client: Client) -> None:
        self._client = client
