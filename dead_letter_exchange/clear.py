import os
import pika

QUEUE = os.environ["QUEUE"]
ROUTING_KEY = os.environ["ROUTING_KEY"]
PRIVATE_URL = os.environ["PRIVATE_URL"]
EXCHANGE_NAME = os.environ["EXCHANGE_NAME"]
DLX_EXCHANGE_NAME = "dlx_exchange"
DLX_QUEUE_NAME = "dlq_queue"


def prepare_rabbitmq():
    # create a connection to RabbitMQ
    connection = pika.BlockingConnection(
        pika.URLParameters(PRIVATE_URL),
    )

    # This is an advanced concept of AMQP;
    # using this abstraction, it is possible to let many different messaging sessions use the same logical connection.
    channel = connection.channel()

    # cleanup
    channel.exchange_delete(EXCHANGE_NAME)
    channel.queue_delete(QUEUE)
    channel.exchange_delete(DLX_EXCHANGE_NAME)
    channel.queue_delete(DLX_QUEUE_NAME)

    # close connection
    channel.close()
    connection.close()


if __name__ == "__main__":
    prepare_rabbitmq()
    print("Cleared")
