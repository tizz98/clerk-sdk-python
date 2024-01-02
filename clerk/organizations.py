from typing import List

from clerk import types
from clerk.client import Service


class OrganizationsService(Service):
    endpoint = "organizations"

    async def list(self) -> List[types.Organization]:
        """Retrieve a list of all organizations"""
        r = await self._client.get(self.endpoint)
        return [types.Organization.model_validate(s) for s in r.json()["data"]]

    async def get(self, organization_id: str) -> types.Organization:
        """Retrieve an organization by their id"""
        r = await self._client.get(f"{self.endpoint}/{organization_id}")
        return types.Organization.model_validate_json(r.content)

    async def delete(self, organization_id: str) -> types.DeleteOrganizationResponse:
        """Delete an organization by their id"""
        r = await self._client.delete(f"{self.endpoint}/{organization_id}")
        return types.DeleteOrganizationResponse.model_validate_json(r.content)

    async def update(
        self, organization_id: str, request: types.UpdateOrganizationRequest
    ) -> types.Organization:
        """Update an organization by their id"""
        r = await self._client.patch(
            f"{self.endpoint}/{organization_id}",
            json=request.model_dump_json(exclude_unset=True),
        )
        return types.Organization.model_validate_json(r.content)
