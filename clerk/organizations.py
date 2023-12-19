from typing import List

from clerk import types
from clerk.client import Service


class OrganizationsService(Service):
    endpoint = "organizations"

    async def list(self) -> List[types.Organization]:
        """Retrieve a list of all organizations"""
        async with self._client.get(self.endpoint) as r:
            s = await r.json()
            return [types.Organization.model_validate(s) for s in s.get("data")]

    async def get(self, organization_id: str) -> types.Organization:
        """Retrieve an organization by their id"""
        async with self._client.get(f"{self.endpoint}/{organization_id}") as r:
            return types.Organization.model_validate(await r.json())

    async def delete(self, organization_id: str) -> types.DeleteOrganizationResponse:
        """Delete an organization by their id"""
        async with self._client.delete(f"{self.endpoint}/{organization_id}") as r:
            return types.DeleteOrganizationResponse.model_validate(await r.json())

    async def update(
        self, organization_id: str, request: types.UpdateOrganizationRequest
    ) -> types.Organization:
        """Update an organization by their id"""
        async with self._client.patch(
            f"{self.endpoint}/{organization_id}", json=request.model_dump_json(exclude_unset=True)
        ) as r:
            return types.Organization.model_validate(await r.json())
