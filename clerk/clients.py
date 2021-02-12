from typing import List

from clerk import types
from clerk.client import Service


class ClientsService(Service):
    endpoint = "clients"
    verify_endpoint = endpoint + "/verify"

    async def list(self) -> List[types.Client]:
        async with self._client.get(self.endpoint) as r:
            return [types.Client.parse_obj(s) for s in await r.json()]

    async def get(self, client_id: str) -> types.Client:
        async with self._client.get(f"{self.endpoint}/{client_id}") as r:
            return types.Client.parse_obj(await r.json())

    async def verify(self, token: str) -> types.Client:
        request = types.VerifyRequest(token=token)

        async with self._client.post(self.verify_endpoint, data=request.json()) as r:
            return types.Client.parse_obj(await r.json())
