from datetime import datetime

import pytz
from sqlalchemy import Engine, create_engine, text
from sqlalchemy.orm import Session

import alembic_runner
from db_models import PMeasurement, PMeasurementType

CONNECTION = "postgresql://postgres:postgres@localhost:5432/postgres"


def get_engine() -> Engine:
    return create_engine(CONNECTION)


def print_all():
    with get_engine().connect() as connection:

        cur = connection.execute(text("SELECT * FROM measurement"))
        rows = cur.all()
        for row in rows:
            print(row)


def test():
    alembic_runner.migrate(get_engine())

    with Session(get_engine()) as session:
        tz = pytz.timezone("Europe/Berlin")
        tsp = datetime.now(tz=tz)
        m = PMeasurement(
            "sensor_1",
            tsp,
            PMeasurementType.HUMIDITY,
            12.34,
        )
        session.add(m)
        session.commit()

    print_all()
