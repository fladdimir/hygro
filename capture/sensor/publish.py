import random
import time

import zmq

import data_models
from measure import measure_humidity, measure_temperature


def run():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    with socket.connect("tcp://127.0.0.1:5554"):
        while True:
            m_temperature = measure_temperature()
            msg = data_models.dump_measurement(m_temperature)
            print(f"{msg}")
            socket.send(str.encode(msg))

            m_humidity = measure_humidity()
            msg = data_models.dump_measurement(m_humidity)
            print(f"{msg}")
            socket.send(str.encode(msg))

            time.sleep(10)
            time.sleep(random.random())


if __name__ == "__main__":
    run()
