from dataclasses import dataclass
from datetime import datetime
from enum import Enum, unique

from marshmallow_dataclass import class_schema


@unique
class MeasurementType(Enum):
    HUMIDITY = "H"
    TEMPERATURE = "T"

    @classmethod
    def from_str(cls, value: str):
        return cls(value)


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


def dump_measurements(ms: list[Measurement]) -> str:
    return _measurement_schema.dumps(ms, many=True)
