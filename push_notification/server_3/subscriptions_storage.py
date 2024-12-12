import os
import asyncio

import subscription_data
from subscription_data import Keys, PushSubscription
from glide import GlideClientConfiguration, NodeAddress, GlideClient


SUBSCRIPTIONS_KEY = "SUBSCRIPTIONS"
VALKEY_HOST = os.getenv("VALKEY_HOST", "localhost")
VALKEY_PORT = int(os.getenv("VALKEY_PORT", "6379"))


def register(subscription: PushSubscription):
    asyncio.run(_save(subscription_data.dump(subscription)))


def get_subscriptions() -> list[PushSubscription]:
    loaded = asyncio.run(_load_all())
    return list(map(subscription_data.load, loaded))


async def _save(subscription: str):
    client = await _get_client()
    await client.sadd(SUBSCRIPTIONS_KEY, [subscription])


async def _load_all() -> set[bytes]:
    client = await _get_client()
    result = await client.smembers(SUBSCRIPTIONS_KEY)
    return result


async def _get_client() -> GlideClient:
    addresses = [
        NodeAddress(VALKEY_HOST, VALKEY_PORT),
    ]
    config = GlideClientConfiguration(addresses)
    client = await GlideClient.create(config)
    return client


if __name__ == "__main__":
    ps = PushSubscription("endpoint_value", Keys("p265dh_value", "auth_value"))
    register(ps)
    print(get_subscriptions())
