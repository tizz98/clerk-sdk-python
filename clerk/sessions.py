from typing import List

from clerk import types
from clerk.client import Service


class SessionsService(Service):
    endpoint = "sessions"

    async def list(self) -> List[types.Session]:
        """Retrieve a list of all sessions"""
        r = await self._client.get(self.endpoint)
        return [types.Session.model_validate(s) for s in r.json()["data"]]

    async def get(self, session_id: str) -> types.Session:
        """Retrieve a session by its id"""
        r = await self._client.get(f"{self.endpoint}/{session_id}")
        return types.Session.model_validate_json(r.content)

    async def revoke(self, session_id: str) -> types.Session:
        """Revoke a session by its id"""
        r = await self._client.post(f"{self.endpoint}/{session_id}/revoke")
        return types.Session.model_validate_json(r.content)
