import datetime
import os

import adafruit_dht
import board
from data_models import Measurement, MeasurementType
from util import retry

SENSOR_PIN_MAPPING = {
    "dht22_1": board.D4,
    "dht22_2": board.D22,
}

SENSOR_ID: str = os.getenv("HYGRO_SENSOR_ID", "")  # "dht22_1"
assert SENSOR_ID != ""
assert SENSOR_ID in SENSOR_PIN_MAPPING
PIN = SENSOR_PIN_MAPPING[SENSOR_ID]
print(f"sensor_id: {SENSOR_ID}, pin: {PIN}")

dht_sensor = adafruit_dht.DHT22(PIN, use_pulseio=False)


def measure_temperature() -> Measurement:
    # deg c
    temperature = _measure_temperature()

    m_temperature = Measurement(
        SENSOR_ID,
        datetime.datetime.now(tz=datetime.timezone.utc),
        MeasurementType.TEMPERATURE,
        temperature,
    )
    return m_temperature


@retry()
def _measure_temperature() -> float:
    measured = dht_sensor.temperature
    if measured is None:
        raise RuntimeError("measurement is None")
    return measured


def measure_humidity() -> Measurement:
    # %
    humidity = _measure_humidity()

    m_humidity = Measurement(
        SENSOR_ID,
        datetime.datetime.now(tz=datetime.timezone.utc),
        MeasurementType.HUMIDITY,
        humidity,
    )
    return m_humidity


@retry()
def _measure_humidity() -> float:
    measured = dht_sensor.humidity
    if measured is None:
        raise RuntimeError("measurement is None")
    return measured
