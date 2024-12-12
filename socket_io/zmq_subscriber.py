import asyncio
import os
from typing import Any, Awaitable, Callable

import zmq.asyncio

import last_n_cache

DEFAULT_SOCKET = "tcp://localhost:5555"
SOCKET_CONNECTION = os.getenv("SOCKET_CONNECTION", DEFAULT_SOCKET)

context = zmq.asyncio.Context()  # type: ignore
socket = context.socket(zmq.SUB)

lnc = last_n_cache.LastNCache(n=1000)


def get_known_messages(max_n=1):
    return lnc.get_latest_messages(max_n=max_n)


async def listen(listener: Callable[[str], Awaitable[Any]]) -> None:
    with socket.connect(SOCKET_CONNECTION):
        print(f"subscribing to [{SOCKET_CONNECTION}]")
        socket.subscribe("")
        while True:
            msg = await socket.recv()
            msg_str = msg.decode()
            lnc.new_message(msg_str)
            await listener(msg_str)
