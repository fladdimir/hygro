from dataclasses import dataclass
from typing import Any, Optional

from marshmallow_dataclass import class_schema


@dataclass
class Keys:
    p256dh: str
    auth: str


@dataclass
class PushSubscription:
    endpoint: str
    keys: Keys
    expirationTime: Optional[Any]


_schema = class_schema(PushSubscription)()


def load(serialized: str | bytes) -> PushSubscription:
    return _schema.loads(serialized)  # type: ignore


def dump(m: PushSubscription) -> str:
    return _schema.dumps(m)
