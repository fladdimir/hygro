import datetime
from datetime import datetime, time, timezone
import math
from time import time as time_s

from dateutil import parser
from flask import Flask
from flask import Response
from flask import request
from sqlalchemy import select, text
from sqlalchemy.orm import Session

from data_models import Measurement, MeasurementType, dump_measurements
from db_models import PMeasurement, map_p_measurement
import db_models
from logger import logger
from sub_store import engine


app = Flask(__name__)


@app.route("/")
def index():
    return "measurements query api"


@app.route("/measurements")
def get_measurements():

    request_args = request.args
    limit = int(request_args.get("limit", 10))

    if "from" in request_args:
        from_time = parser.parse(request_args["from"])
    else:
        start_of_day = datetime.combine(datetime.now(), time.min, tzinfo=timezone.utc)
        from_time = start_of_day
    if "to" in request_args:
        to_time = parser.parse(request_args["to"])
    else:
        end_of_day = datetime.combine(datetime.now(), time.max, tzinfo=timezone.utc)
        to_time = end_of_day

    criterion = (PMeasurement.tsp >= from_time) & (PMeasurement.tsp <= to_time)

    if "type" in request_args:
        measurement_type_arg = request_args["type"]
        try:
            measurement_type = MeasurementType[measurement_type_arg]
        except KeyError:
            return Response(f"invalid type: {measurement_type_arg}", status=404)
        p_measurement_type = db_models.measurement_type_map[measurement_type]
        criterion = criterion & (PMeasurement.measurement_type == p_measurement_type)

    if "sensor_ids" in request_args:
        sensor_ids = request_args["sensor_ids"].split(",")
        criterion = criterion & (PMeasurement.sensor_id.in_(sensor_ids))

    with Session(engine) as session:
        query_start = time_s()
        pmeasurements = session.scalars(
            select(PMeasurement)
            .where(criterion)
            .order_by(PMeasurement.tsp.desc())
            .limit(limit)
        ).all()
    query_end = time_s() - query_start
    logger.info(f"sqlalchemy query duration {query_end:.3f}s")
    measurements = [map_p_measurement(p) for p in pmeasurements]

    measurements_json = dump_measurements(measurements)
    response = Response(
        response=measurements_json, status=200, mimetype="application/json"
    )
    return response


@app.route("/measurements-time-buckets")
def get_measurements_time_buckets():

    request_args = request.args

    limit = int(request_args.get("limit", 10))

    from_time: datetime
    if "from" in request_args:
        from_time = parser.parse(request_args["from"])
    else:
        start_of_day = datetime.combine(datetime.now(), time.min, tzinfo=timezone.utc)
        from_time = start_of_day
    to_time: datetime
    if "to" in request_args:
        to_time = parser.parse(request_args["to"])
    else:
        end_of_day = datetime.combine(datetime.now(), time.max, tzinfo=timezone.utc)
        to_time = end_of_day
    if "type" in request_args:
        measurement_type_arg = request_args["type"]
        try:
            measurement_type = MeasurementType[measurement_type_arg]
        except KeyError:
            return Response(f"invalid type: {measurement_type_arg}", status=404)
    else:
        measurement_type = MeasurementType.TEMPERATURE
    p_measurement_type = db_models.measurement_type_map[measurement_type]
    sensor_ids: list[str] | None = None
    if "sensor_ids" in request_args:
        sensor_ids = request_args["sensor_ids"].split(",")

    time_span_s = (to_time - from_time).total_seconds()
    bucket_size_s = math.ceil(time_span_s / limit)
    bucket_size_s_half = math.ceil(bucket_size_s / 2)
    query_str = f"""
SELECT
time_bucket('{bucket_size_s} s', tsp) + '{bucket_size_s_half} s' as bucket,
avg(value) as value
FROM
measurement
WHERE
measurement.measurement_type = '{p_measurement_type.name}'
AND
measurement.tsp <= '{to_time}'::timestamptz
AND
measurement.tsp >= '{from_time}'::timestamptz
{"" if sensor_ids is None else "AND measurement.sensor_id in :sensor_ids"}
GROUP BY bucket
ORDER BY bucket DESC;
    """
    with Session(engine) as session:
        query_start = time_s()
        rows = session.execute(
            text(query_str),
            {"sensor_ids": tuple(sensor_ids) if sensor_ids is not None else None},
        ).all()
    query_end = time_s() - query_start
    logger.info(f"sqlalchemy query duration {query_end:.3f}s")

    sensor_id = ",".join(sensor_ids) if sensor_ids is not None else "na"
    measurements = [
        Measurement(
            sensor_id=sensor_id,
            tsp=row.bucket,  # type: ignore
            measurement_type=measurement_type,
            value=row.value,  # type: ignore
        )
        for row in rows
    ]

    measurements_json = dump_measurements(measurements)
    response = Response(
        response=measurements_json, status=200, mimetype="application/json"
    )
    return response


if __name__ == "__main__":
    app.run("0.0.0.0", 5000, debug=True, threaded=False, use_reloader=False)
