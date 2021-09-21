# https://www.cloudamqp.com/docs/http.html
# you can publish messages via http, no need to use rabbit mq directly

import os
import json
import requests
from requests.auth import HTTPBasicAuth
from urllib.parse import urlparse
from typing import Dict, Optional
from dataclasses import dataclass, asdict

PRIVATE_URL = os.environ["PRIVATE_URL"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]


@dataclass
class PublishData:
    routing_key: str
    payload: Dict
    payload_encoding: str
    properties: Optional[Dict]


def publish():
    message = PublishData(
        routing_key=ROUTING_KEY,
        payload=json.dumps(
            {
                "booking_request_id": 1,
            }
        ),
        payload_encoding="string",
        # delivery_mode is required
        properties={
            "delivery_mode": 1,
        },
    )

    url_parsed = urlparse(PRIVATE_URL)

    # url pattern
    # https://username:password@hostname/api/exchanges/vhost/amq.default/publish
    url_without_username_and_password = (
        "https://"
        + url_parsed.hostname
        + "/api/exchanges"
        # url_parsed.path is vhost
        + f"{url_parsed.path}/{EXCHANGE_NAME}/publish"
    )

    response = requests.post(
        url=url_without_username_and_password,
        json=asdict(message),
        auth=HTTPBasicAuth(
            username=url_parsed.username,
            password=url_parsed.password,
        ),
    )

    print(response.url)
    print(response.request.body)

    print("-" * 20)

    print(response.status_code)
    print(response.content)
    print(response.reason)

    print("-" * 20)


if __name__ == "__main__":
    publish()
