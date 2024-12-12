import datetime
import os
import random
import time

import zmq

import data_models

SENSOR_ID = os.getenv("HYGRO_SENSOR_ID", "sensor_1")
print(f"SENSOR_ID: {SENSOR_ID}")

context = zmq.Context()
socket = context.socket(zmq.PUB)
with socket.connect("tcp://127.0.0.1:5554"):
    for i in range(100_000_000):

        m = data_models.Measurement(
            SENSOR_ID,
            datetime.datetime.now(tz=datetime.timezone.utc),
            data_models.MeasurementType.TEMPERATURE,
            random.randint(0, 30),  # i % 10,
        )
        msg = data_models.dump_measurement(m)
        print(f"publishing: {msg}")
        socket.send(str.encode(msg))
        time.sleep(random.random())

        m = data_models.Measurement(
            SENSOR_ID,
            datetime.datetime.now(tz=datetime.timezone.utc),
            data_models.MeasurementType.HUMIDITY,
            random.randint(0, 100),  # (i + 3) % 10,
        )
        msg = data_models.dump_measurement(m)
        print(f"{msg}")
        socket.send(str.encode(msg))
        time.sleep(random.random())
