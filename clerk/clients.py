from typing import List

from clerk import types
from clerk.client import Service


class ClientsService(Service):
    endpoint = "clients"
    verify_endpoint = endpoint + "/verify"

    async def list(self) -> List[types.Client]:
        """Retrieve a list of all clients"""
        r = await self._client.get(self.endpoint)
        return [types.Client.model_validate(s) for s in r.json()["data"]]

    async def get(self, client_id: str) -> types.Client:
        """Retrieve a client by its id"""
        r = await self._client.get(f"{self.endpoint}/{client_id}")
        return types.Client.model_validate_json(r.content)

    async def verify(self, token: str) -> types.Client:
        """Verify a token and return its associated client, if valid"""
        request = types.VerifyRequest(token=token)

        r = await self._client.post(self.verify_endpoint, request=request)
        return types.Client.model_validate_json(r.content)
