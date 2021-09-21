import os
import pika
from pika.adapters.blocking_connection import BlockingChannel

QUEUE = os.environ["QUEUE"]
PRIVATE_URL = os.environ["PRIVATE_URL"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]
REPLY_QUEUE = "amq.rabbitmq.reply-to"


def on_message(channel: BlockingChannel, method_frame, header_frame, body):
    print(f"Thanks for response, {body}")


def consumer_start():
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )
    channel = connection.channel()

    # consume reply queue
    channel.basic_consume(
        REPLY_QUEUE,
        on_message,
        auto_ack=True,
    )

    # publish to service queue
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE,
        body="2",
        properties=pika.BasicProperties(reply_to=REPLY_QUEUE),
    )

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    # close connection
    channel.close()
    connection.close()


if __name__ == "__main__":
    consumer_start()
