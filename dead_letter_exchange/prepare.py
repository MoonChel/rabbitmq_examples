import os
import pika
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel

QUEUE = os.environ["QUEUE"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
PRIVATE_URL = os.environ["PRIVATE_URL"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]
DLX_EXCHANGE_NAME = "dlx_exchange"
DLX_QUEUE_NAME = "dlq_queue"


def prepare_processing(channel: BlockingChannel):
    # cleanup
    channel.exchange_delete(EXCHANGE_NAME)
    channel.queue_delete(QUEUE)

    # setup processing
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
        arguments={
            "x-dead-letter-exchange": DLX_EXCHANGE_NAME,
            # if not specified, queue's routing-key is used
            # "x-dead-letter-routing-key": ROUTING_KEY,
        },
    )

    channel.queue_bind(QUEUE, EXCHANGE_NAME, routing_key=ROUTING_KEY)


def prepare_dead_letter(channel: BlockingChannel):
    # cleanup
    channel.exchange_delete(DLX_EXCHANGE_NAME)
    channel.queue_delete(DLX_QUEUE_NAME)

    # setup dead letter
    channel.exchange_declare(
        DLX_EXCHANGE_NAME,
        exchange_type=ExchangeType.direct,
    )

    channel.queue_declare(DLX_QUEUE_NAME)

    channel.queue_bind(
        DLX_QUEUE_NAME,
        DLX_EXCHANGE_NAME,
        ROUTING_KEY,
    )


def prepare_rabbitmq():
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )

    # This is an advanced concept of AMQP;
    # using this abstraction, it is possible to let many different messaging sessions use the same logical connection.
    channel = connection.channel()

    prepare_processing(channel)

    prepare_dead_letter(channel)

    # close connection
    channel.close()
    connection.close()


if __name__ == "__main__":
    prepare_rabbitmq()
    print("Done")
