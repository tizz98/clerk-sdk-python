from . import types
from .client import Service


class SessionsService(Service):
    endpoint = "sessions"

    async def list(self) -> list[types.Session]:
        """Retrieve a list of all sessions"""
        async with self._client.get(self.endpoint) as r:
            return [types.Session.model_validate(s) for s in await r.json()]

    async def get(self, session_id: str) -> types.Session:
        """Retrieve a session by its id"""
        async with self._client.get(f"{self.endpoint}/{session_id}") as r:
            return types.Session.model_validate(await r.json())

    async def revoke(self, session_id: str) -> types.Session:
        """Revoke a session by its id"""
        async with self._client.post(f"{self.endpoint}/{session_id}/revoke") as r:
            return types.Session.model_validate(await r.json())

    async def verify(self, session_id: str, token: str) -> types.Session:
        """Verify a session by its id and a given token"""
        request = types.VerifyRequest(token=token)

        async with self._client.post(
            f"{self.endpoint}/{session_id}/verify", data=request.json()
        ) as r:
            return types.Session.model_validate(await r.json())
