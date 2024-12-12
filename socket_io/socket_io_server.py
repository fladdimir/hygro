import asyncio

from aiohttp import web
import socketio

import zmq_subscriber

sio = socketio.AsyncServer(cors_allowed_origins="*")
app = web.Application()
sio.attach(app)

connections = set()


@sio.event
def connect(sid, environ):
    print("connect ", sid)
    connections.add(sid)
    asyncio.get_running_loop().create_task(replay(sid))


@sio.event
def disconnect(sid):
    print("disconnect ", sid)
    connections.remove(sid)


async def handle_message(msg: str):
    await sio.emit("data", msg)


async def replay(sid: str, max_n=1000):
    known_messages = zmq_subscriber.get_known_messages(max_n)
    for msg in known_messages:
        await sio.emit("data", data=msg, to=sid)


async def index(request):
    return web.Response(text="zmq-sio", content_type="text/plain")


app.router.add_get("/", index)


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    loop.create_task(zmq_subscriber.listen(handle_message))
    web.run_app(app, host="0.0.0.0", port=3000, loop=loop)
    loop.run_forever()
