import json
import os

from pywebpush import webpush

from data_models import Measurement
import subscription_data
import subscriptions_storage


VAPID_PUBLIC_KEY = os.getenv("VAPID_PUBLIC_KEY")
VAPID_PRIVATE_KEY = os.getenv("VAPID_PRIVATE_KEY")
VAPID_SUBJECT = os.getenv("VAPID_SUBJECT")

if not VAPID_PUBLIC_KEY:
    raise Exception("VAPID_PUBLIC_KEY not set")
if not VAPID_PRIVATE_KEY:
    raise Exception("VAPID_PRIVATE_KEY not set")
if not VAPID_SUBJECT:
    raise Exception("VAPID_SUBJECT not set")


def get_public_key() -> str:
    return VAPID_PUBLIC_KEY  # type: ignore


def notify_subscriber(measurement: Measurement):

    subscriptions = subscriptions_storage.get_subscriptions()

    print(f"alert received, notifying {len(subscriptions)} subscriber(s)")

    for subscription in subscriptions:
        webpush(
            subscription_info=json.loads(subscription_data.dump(subscription)),
            vapid_private_key=VAPID_PRIVATE_KEY,
            vapid_claims={"sub": VAPID_SUBJECT},  # type: ignore
            data=f"Hygro alert {measurement.tsp.strftime('%d.%m.%Y, %H:%M:%S')} : {measurement.value}%",
        )
