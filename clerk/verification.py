from typing import Optional

from clerk import errors, types
from clerk.client import Service


class VerificationService(Service):
    async def verify(self, session_token: str, session_id: Optional[str] = None) -> types.Session:
        if not session_id:
            client = await self._client.clients.verify(session_token)
            if not client.last_active_session_id:
                raise errors.NoActiveSessionException(client.id)
            return await self._client.session.get(client.last_active_session_id)
        return await self._client.session.verify(session_id, session_token)
