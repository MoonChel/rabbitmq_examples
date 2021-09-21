import os
import pika
from pika.adapters.blocking_connection import BlockingChannel

QUEUE = os.environ["QUEUE"]
PRIVATE_URL = os.environ["PRIVATE_URL"]


def on_message(channel: BlockingChannel, method_frame, properties, body):
    number = int(body)

    channel.basic_publish(
        "",
        routing_key=properties.reply_to,
        body=str(number ** 2),
    )


def consumer_start():
    print("consumer starts...")
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )
    channel = connection.channel()

    channel.basic_consume(
        QUEUE,
        on_message,
        auto_ack=True,
        consumer_tag="our-consumer",
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
