from typing import List

from clerk import types
from clerk.client import Service


class SessionsService(Service):
    endpoint = "sessions"

    async def list(self) -> List[types.Session]:
        async with self._client.get(self.endpoint) as r:
            return [types.Session.parse_obj(s) for s in await r.json()]

    async def get(self, session_id: str) -> types.Session:
        async with self._client.get(f"{self.endpoint}/{session_id}") as r:
            return types.Session.parse_obj(await r.json())

    async def revoke(self, session_id: str) -> types.Session:
        async with self._client.post(f"{self.endpoint}/{session_id}/revoke") as r:
            return types.Session.parse_obj(await r.json())

    async def verify(self, session_id: str, token: str) -> types.Session:
        request = types.VerifyRequest(token=token)

        async with self._client.post(
            f"{self.endpoint}/{session_id}/verify", data=request.json()
        ) as r:
            return types.Session.parse_obj(await r.json())
