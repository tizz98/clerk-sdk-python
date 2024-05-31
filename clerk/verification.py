from . import errors, types
from .client import Service


class VerificationService(Service):
    async def verify(
        self, session_token: str, session_id: str | None = None
    ) -> types.Session:
        """Verify a session token and return the associated session, if any.

        If a session_id is not passed then the client's last active session is returned.
        """
        if not session_id:
            client = await self._client.clients.verify(session_token)
            if not client.last_active_session_id:
                raise errors.NoActiveSessionException(client.id)
            return await self._client.session.get(client.last_active_session_id)
        return await self._client.session.verify(session_id, session_token)
