import json
from .tasks import send_confirmation_email_for_host, send_feedback_email_to_customer


ROUTER = {
    "send_feedback_email_to_customer": send_feedback_email_to_customer,
    "send_confirmation_email_for_host": send_confirmation_email_for_host,
}


class ActionNotFound(Exception):
    pass


def on_message(channel, method_frame, header_frame, body):
    # or apply pydantic rightaway
    json_body = json.loads(body)

    if not json_body["action"] in ROUTER:
        raise ActionNotFound(json_body["action"])

    results = ROUTER[json_body](json_body["kwargs"])

    # store results if needed
