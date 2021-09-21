import os
import pika
from pika.exchange_type import ExchangeType

QUEUE = os.environ["QUEUE"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
PRIVATE_URL = os.environ["PRIVATE_URL"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]


def prepare_rabbitmq():
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )

    # This is an advanced concept of AMQP;
    # using this abstraction, it is possible to let many different messaging sessions use the same logical connection.
    channel = connection.channel()

    # cleanup
    channel.exchange_delete(EXCHANGE_NAME)
    channel.queue_delete(QUEUE)

    # setup
    channel.exchange_declare(
        EXCHANGE_NAME,
        exchange_type=ExchangeType.direct,
        # Survive a reboot of RabbitMQ
        durable=True,
        # create if does not exists
        # passive=True,
    )

    channel.queue_declare(
        QUEUE,
        # create if does not exists
        # passive=True,
        # Survive a reboot of RabbitMQ
        durable=True,
    )

    channel.queue_bind(QUEUE, EXCHANGE_NAME, routing_key=ROUTING_KEY)

    # close connection
    channel.close()
    connection.close()


if __name__ == "__main__":
    prepare_rabbitmq()
    print("Done")
