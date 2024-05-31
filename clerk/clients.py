from . import types
from .client import Service


class ClientsService(Service):
    endpoint = "clients"
    verify_endpoint = endpoint + "/verify"

    async def list(self) -> list[types.Client]:
        """Retrieve a list of all clients"""
        async with self._client.get(self.endpoint) as r:
            return [types.Client.model_validate(s) for s in await r.json()]

    async def get(self, client_id: str) -> types.Client:
        """Retrieve a client by its id"""
        async with self._client.get(f"{self.endpoint}/{client_id}") as r:
            return types.Client.model_validate(await r.json())

    async def verify(self, token: str) -> types.Client:
        """Verify a token and return its associated client, if valid"""
        request = types.VerifyRequest(token=token)

        async with self._client.post(self.verify_endpoint, data=request.json()) as r:
            return types.Client.model_validate(await r.json())
