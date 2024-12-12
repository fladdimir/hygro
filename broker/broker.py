import asyncio

import zmq.asyncio

context = zmq.asyncio.Context()  # type: ignore

sub_socket = context.socket(zmq.SUB)
pub_socket = context.socket(zmq.PUB)


async def forward():
    with sub_socket.bind("tcp://0.0.0.0:5554"), pub_socket.bind("tcp://0.0.0.0:5555"):
        sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        print("listening...")
        while True:
            msg = await sub_socket.recv()
            await pub_socket.send(msg)


if __name__ == "__main__":
    asyncio.run(forward())
