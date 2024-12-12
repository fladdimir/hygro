import os
from typing import Callable

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import zmq
import zmq

import alembic_runner
import data_models
import db_models
from logger import logger


DEFAULT_CONNECTION = "postgresql://postgres:postgres@localhost:5432/postgres"
CONNECTION = os.getenv("DB_CONNECTION", DEFAULT_CONNECTION)
engine = create_engine(CONNECTION, echo=False)

DEFAULT_SOCKET = "tcp://localhost:5555"
SOCKET_CONNECTION = os.getenv("SOCKET_CONNECTION", DEFAULT_SOCKET)


def store(pm: db_models.PMeasurement) -> None:
    with Session(engine) as session:
        session.add(pm)
        session.commit()
    logger.debug("measurement stored")


def map_and_store(measurement_str: str) -> None:
    m = data_models.load_measurement(measurement_str)
    pm = db_models.map_measurement(m)
    try:
        store(pm)
    except Exception as ex:
        logger.error(ex)


def listen(socket: zmq.SyncSocket, consumer: Callable[[str], None]) -> None:
    while True:
        msg = socket.recv()
        msg_str = msg.decode()
        logger.debug("message received: %s", msg_str)
        consumer(msg_str)


def sub() -> zmq.SyncSocket:
    context = zmq.Context()
    socket: zmq.SyncSocket = context.socket(zmq.SUB)
    socket.connect(SOCKET_CONNECTION)
    socket.setsockopt(zmq.SUBSCRIBE, b"")
    return socket


def start_listening():
    socket = sub()
    logger.info(f"starting to listen to [{SOCKET_CONNECTION}]...")
    listen(socket, map_and_store)


if __name__ == "__main__":

    alembic_runner.migrate(engine)

    start_listening()
