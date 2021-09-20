import os
import pika

QUEUE = os.environ["QUEUE"]
PRIVATE_URL = os.environ["PRIVATE_URL"]


def on_message(channel, method_frame, header_frame, body):
    print(channel)
    print(body)


def consumer_start():
    print("consumer starts...")
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )
    channel = connection.channel()

    channel.basic_consume(QUEUE, on_message, auto_ack=True, consumer_tag="our-consumer")

    try:
        channel.start_consuming()
    except KeyboardInterrupt:
        channel.stop_consuming()

    connection.close()


if __name__ == "__main__":
    consumer_start()
