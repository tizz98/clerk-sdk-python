# Unofficial Clerk.dev Python SDK

## What is Clerk.dev?

See https://clerk.dev

## Installation

`pip install clerk-sdk-python`

## Usage

```python
import asyncio

from clerk import Client


async def main():
    async with Client("my-token") as client:
        users = await client.users.list()
        for user in users:
            print(f"Got user {user.id} -> {user.first_name} {user.last_name}")


asyncio.run(main())
```
