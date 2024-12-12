import asyncio
import data_models
import zmq.asyncio
import os

DEFAULT_SOCKET = "tcp://localhost:5555"
SOCKET_CONNECTION = os.getenv("SOCKET_CONNECTION", DEFAULT_SOCKET)

context = zmq.asyncio.Context()  # type: ignore

sub_socket = context.socket(zmq.SUB)
pub_socket = context.socket(zmq.PUB)

# 2 step controller for avg of last n values

CONTROLLED_MEASUREMENT_TYPES = {data_models.MeasurementType.HUMIDITY}

UPPER_THRESHOLDS = {data_models.MeasurementType.HUMIDITY: 61}
LOWER_THRESHOLDS = {data_models.MeasurementType.HUMIDITY: 55}
N_VALUES = 5

last_measurements: dict[data_models.MeasurementType, list[float]] = {
    mt: [] for mt in data_models.MeasurementType
}

# (over thresholds -> true)
current_state = {mt: False for mt in data_models.MeasurementType}


def is_notification_change(m: data_models.Measurement) -> bool:
    # switch of current state false -> true

    if not m.measurement_type in CONTROLLED_MEASUREMENT_TYPES:
        return False

    last_values = last_measurements[m.measurement_type]
    if len(last_values) > N_VALUES:
        last_values.pop(0)
    last_values.append(m.value)

    if len(last_values) < N_VALUES:
        return False  # not yet enough data

    avg = sum(last_values) / len(last_values)
    avg_over_upper = avg > UPPER_THRESHOLDS[m.measurement_type]
    avg_under_lower = avg < LOWER_THRESHOLDS[m.measurement_type]

    if avg_over_upper and not current_state[m.measurement_type]:
        current_state[m.measurement_type] = True
        print(f"HIGH at {m.tsp}, avg: {avg}")
        return True

    if avg_under_lower and current_state[m.measurement_type]:
        print(f"LOW at {m.tsp}, avg: {avg}")
        current_state[m.measurement_type] = False

    return False


async def subscribe():

    with sub_socket.connect(SOCKET_CONNECTION), pub_socket.bind("tcp://0.0.0.0:5556"):
        sub_socket.setsockopt(zmq.SUBSCRIBE, b"")
        print("listening (stream analysis)...")
        while True:
            msg = await sub_socket.recv()
            msg_str = msg.decode()
            m = data_models.load_measurement(msg_str)
            if is_notification_change(m):
                await pub_socket.send(msg)


if __name__ == "__main__":
    asyncio.run(subscribe())
