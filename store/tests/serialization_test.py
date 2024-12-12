import datetime

from data_models import Measurement, MeasurementType, dump_measurement, load_measurement


def test_serialization():
    m = Measurement(
        "sensor_1", datetime.datetime.now(), MeasurementType.TEMPERATURE, 43.21
    )

    m_serialized = dump_measurement(m)
    m_deserialized = load_measurement(m_serialized)
    m_serialized_2 = dump_measurement(m_deserialized)

    assert m == m_deserialized
    assert m_serialized == m_serialized_2
