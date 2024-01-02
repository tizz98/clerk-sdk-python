from typing import List

from clerk import types
from clerk.client import Service


class UsersService(Service):
    endpoint = "users"

    async def list(self) -> List[types.User]:
        """Retrieve a list of all users"""
        r = await self._client.get(self.endpoint)
        return [types.User.model_validate(s) for s in r.json()["data"]]

    async def get(self, user_id: str) -> types.User:
        """Retrieve a user by their id"""
        r = await self._client.get(f"{self.endpoint}/{user_id}")
        return types.User.model_validate_json(r.content)

    async def delete(self, user_id: str) -> types.DeleteUserResponse:
        """Delete a user by their id"""
        r = await self._client.delete(f"{self.endpoint}/{user_id}")
        return types.DeleteUserResponse.model_validate_json(r.content)

    async def update(self, user_id: str, request: types.UpdateUserRequest) -> types.User:
        """Update a user by their id"""
        r = await self._client.patch(
            f"{self.endpoint}/{user_id}",
            json=request.model_dump_json(exclude_unset=True),
        )
        return types.User.model_validate_json(r.content)

    async def memberships(self, user_id: str) -> List[types.OrganizationMembership]:
        """Retrieve a list of all memberships for a user"""
        r = await self._client.get(f"{self.endpoint}/{user_id}/memberships")
        return [types.OrganizationMembership.model_validate(s) for s in r.json()["data"]]
