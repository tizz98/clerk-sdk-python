import aiohttp

from . import types

__all__ = ["ClerkAPIException", "NoActiveSessionException"]


class ClerkAPIException(Exception):
    def __init__(
        self, status: int, method: str, url: str, *api_errors: types.Error
    ) -> None:
        self.status = status
        self.method = method
        self.url = url
        self.api_errors = api_errors
        super().__init__(f"{self.method} {self.url}: {self.status} {self.api_errors!r}")

    @classmethod
    async def from_response(cls, resp: aiohttp.ClientResponse) -> "ClerkAPIException":
        try:
            data = await resp.json()
        except:  # noqa
            api_errors = []
        else:
            errors = data.get("errors", [])
            api_errors = [types.Error.model_validate(e) for e in errors]

        return ClerkAPIException(resp.status, resp.method, str(resp.url), *api_errors)


class NoActiveSessionException(Exception):
    def __init__(self, client_id: str):
        super().__init__(f"no active sessions for given client {client_id}")
