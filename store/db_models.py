from dataclasses import dataclass
from datetime import datetime
import enum

from sqlalchemy import DateTime, Numeric
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass, mapped_column

from data_models import Measurement, MeasurementType


class SqlaBase(DeclarativeBase, MappedAsDataclass):
    pass


class PMeasurementType(enum.Enum):
    HUMIDITY = "H"
    TEMPERATURE = "T"


@dataclass
class PMeasurement(SqlaBase):
    __tablename__ = "measurement"

    sensor_id: Mapped[str] = mapped_column(primary_key=True)
    tsp: Mapped[datetime] = mapped_column(DateTime(timezone=True), primary_key=True)
    measurement_type: Mapped[PMeasurementType] = mapped_column(primary_key=True)
    value: Mapped[float] = mapped_column(Numeric(6, 3))


measurement_type_map = {
    MeasurementType.TEMPERATURE: PMeasurementType.TEMPERATURE,
    MeasurementType.HUMIDITY: PMeasurementType.HUMIDITY,
}

p_measurement_type_map = {
    PMeasurementType.TEMPERATURE: MeasurementType.TEMPERATURE,
    PMeasurementType.HUMIDITY: MeasurementType.HUMIDITY,
}


def map_measurement(m: Measurement) -> PMeasurement:
    return PMeasurement(
        sensor_id=m.sensor_id,
        tsp=m.tsp,
        measurement_type=measurement_type_map[m.measurement_type],
        value=m.value,
    )


def map_p_measurement(p: PMeasurement) -> Measurement:
    return Measurement(
        sensor_id=p.sensor_id,
        tsp=p.tsp,
        measurement_type=p_measurement_type_map[p.measurement_type],
        value=p.value,
    )
