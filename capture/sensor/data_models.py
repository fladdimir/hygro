from dataclasses import dataclass
from datetime import datetime
from enum import Enum

from marshmallow_dataclass import class_schema


class MeasurementType(Enum):
    HUMIDITY = "H"
    TEMPERATURE = "T"


@dataclass
class Measurement:
    sensor_id: str
    tsp: datetime
    measurement_type: MeasurementType
    value: float


_measurement_schema = class_schema(Measurement)()


def load_measurement(serialized: str) -> Measurement:
    return _measurement_schema.loads(serialized)  # type: ignore


def dump_measurement(m: Measurement) -> str:
    return _measurement_schema.dumps(m)
