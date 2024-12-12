import os
from typing import Callable
import data_models
import zmq
import notification_sender

DEFAULT_SOCKET = "tcp://localhost:5556"
SOCKET_CONNECTION = os.getenv("SOCKET_CONNECTION", DEFAULT_SOCKET)


def _map_and_notify(measurement_str: str) -> None:
    measurement = data_models.load_measurement(measurement_str)
    notification_sender.notify_subscriber(measurement)


def _listen(socket: zmq.SyncSocket, consumer: Callable[[str], None]) -> None:
    while True:
        msg = socket.recv()
        msg_str = msg.decode()
        consumer(msg_str)


def _sub() -> zmq.SyncSocket:
    context = zmq.Context()
    socket: zmq.SyncSocket = context.socket(zmq.SUB)
    socket.connect(SOCKET_CONNECTION)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    return socket


def start_listening():
    socket = _sub()
    _listen(socket, _map_and_notify)


def run():
    start_listening()
