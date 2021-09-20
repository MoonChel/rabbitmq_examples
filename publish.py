import os
import pika

PRIVATE_URL = os.environ["PRIVATE_URL"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]


def publish():
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )
    channel = connection.channel()

    channel.basic_publish(
        exchange=EXCHANGE_NAME,
        routing_key=ROUTING_KEY,
        body="Hello World!",
    )

    # close connection
    connection.close()


if __name__ == "__main__":
    publish()
