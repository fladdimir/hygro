from flask import Flask
from flask import Response
from flask import request

import notification_sender
import subscription_data
import subscriptions_storage

app = Flask(__name__)


BASE_PATH = "/push-notifications"


@app.get(BASE_PATH + "/")
def index():
    return "push notifications api"


@app.get(BASE_PATH + "/vapid-public-key")
def get_vapid_public_key():
    return notification_sender.get_public_key()


@app.post(BASE_PATH + "/register-subscription")
def register_subscription():
    data = request.data
    parsed = subscription_data.load(data)
    subscriptions_storage.register(parsed)
    return Response(status=201)


def run():
    app.run("0.0.0.0", 3002, debug=False)


if __name__ == "__main__":
    run()
