import os
import json
import pika

import rollbar

from .tasks import send_confirmation_email_for_host, send_feedback_email_to_customer

ROUTER = {
    "send_feedback_email_to_customer": send_feedback_email_to_customer,
    "send_confirmation_email_for_host": send_confirmation_email_for_host,
}

QUEUE = os.environ["QUEUE"]
PRIVATE_URL = os.environ["PRIVATE_URL"]

rollbar = None


class ActionNotFound(Exception):
    pass


def on_message(channel, method_frame, header_frame, body):
    # or apply pydantic rightaway
    json_body = json.loads(body)

    if not json_body["action"] in ROUTER:
        raise ActionNotFound(json_body["action"])

    try:
        # store results if needed
        results = ROUTER[json_body](json_body["kwargs"])
    except:
        # catch exception with context to rollbar
        rollbar.report_exc_info(extra_data=json_body)
        channel.basic_nack()


def consumer_start():
    print("consumer starts...")
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )
    channel = connection.channel()

    channel.basic_consume(QUEUE, on_message, consumer_tag="our-consumer")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # close connection
    channel.close()
    connection.close()
