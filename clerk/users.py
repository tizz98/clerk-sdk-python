from typing import List

from clerk import types
from clerk.client import Service


class UsersService(Service):
    endpoint = "users"

    async def list(self) -> List[types.User]:
        async with self._client.get(self.endpoint) as r:
            return [types.User.parse_obj(s) for s in await r.json()]

    async def get(self, user_id: str) -> types.User:
        async with self._client.get(f"{self.endpoint}/{user_id}") as r:
            return types.User.parse_obj(await r.json())

    async def delete(self, user_id: str) -> types.DeleteUserResponse:
        async with self._client.delete(f"{self.endpoint}/{user_id}") as r:
            return types.DeleteUserResponse.parse_obj(await r.json())

    async def update(self, user_id: str, request: types.UpdateUserRequest) -> types.User:
        async with self._client.patch(
            f"{self.endpoint}/{user_id}", data=request.json(exclude_unset=True)
        ) as r:
            return types.User.parse_obj(await r.json())
