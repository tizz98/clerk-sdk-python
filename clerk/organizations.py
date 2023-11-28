from typing import List

from clerk import types
from clerk.client import Service


class OrganizationsService(Service):
    endpoint = "organizations"

    async def list(self) -> List[types.Organization]:
        """Retrieve a list of all organizations"""
        async with self._client.get(self.endpoint) as resp:
            resp_json = await resp.json()
            return [types.Organization.parse_obj(obj) for obj in resp_json.get("data", [])]

    async def get(self, organization_id: str) -> types.Organization:
        """Retrieve an organization by their id"""
        async with self._client.get(f"{self.endpoint}/{organization_id}") as resp:
            return types.Organization.parse_obj(await resp.json())

    async def delete(self, organization_id: str) -> types.DeleteOrganizationResponse:
        """Delete an organization by their id"""
        async with self._client.delete(f"{self.endpoint}/{organization_id}") as resp:
            return types.DeleteOrganizationResponse.parse_obj(await resp.json())

    async def update(self, organization_id: str, request: types.UpdateOrganizationRequest) -> types.Organization:
        """Update an organization by their id"""
        async with self._client.patch(
            f"{self.endpoint}/{organization_id}", data=request.json(exclude_unset=True)
        ) as resp:
            return types.Organization.parse_obj(await resp.json())
