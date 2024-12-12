from dataclasses import dataclass, field

from data_models import MeasurementType, load_measurement


@dataclass()
class LastNCache:
    n: int

    cache: dict[MeasurementType, list[str]] = field(default_factory=dict)

    def new_message(self, msg: str) -> None:
        m = load_measurement(msg)
        m_list: list[str] = self._get_m_list(m.measurement_type)
        m_list.append(msg)
        while len(m_list) > self.n:
            m_list.pop(0)

    def _get_m_list(self, m_type: MeasurementType) -> list[str]:
        if m_type not in self.cache:
            self.cache[m_type] = []
        return self.cache[m_type]

    def get_latest_messages(self, max_n=1) -> list[str]:
        values = []
        for m_type in MeasurementType:
            m_list = self._get_m_list(m_type)
            n = min(len(m_list), max_n)
            recent_values = m_list[-n:]
            values.extend(recent_values)
        return values
