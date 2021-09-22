## Setup

1. create new virtualenv
2. pip install -r requirements.in
3. pip install python-dotenv
4. create .env file with vars
    - EXCHANGE_NAME
    - QUEUE
    - ROUTING_KEY
    - PRIVATE_URL
5. Run prepare.py from a specific folder to configure RabbitMQ

## Run examples

### Basic consumer and publisher in 2 independent terminals
```shell
    dotenv -f .env run -- python basic/prepare.py
    dotenv -f .env run -- python basic/consume.py
    dotenv -f .env run -- python basic/publish.py
    dotenv -f .env run -- python basic/publish_http.py
```

### Remote procedure call

- https://www.rabbitmq.com/direct-reply-to.html

```shell
    dotenv -f .env run -- python remote_procedure_call/rpc_consume.py
    dotenv -f .env run -- python remote_procedure_call/rpc_publish_consume.py
```

![Remote procedure call](https://github.com/MoonChel/rabbitmq_examples/blob/37f7692d256a75788e62d66d3136fa73bf1bfba2/images/remote_procedure_call.png)


### Plan and execute tasks in future

![Task planning](https://github.com/MoonChel/rabbitmq_examples/blob/adf68311e03ad7f74a6823ca1bc761dc89f719b7/images/task_planning_for_future.png)

### Dead letter exchange

- https://www.rabbitmq.com/dlx.html

![Dead letter exchange](https://github.com/MoonChel/rabbitmq_examples/blob/dd5fb43b02a662bcfea8462146bc5d91703ed7e3/images/dead_letter_queue.png)

```shell
    dotenv -f .env run -- python dead_letter_exchange/prepare.py
    dotenv -f .env run -- python dead_letter_exchange/publish_http.py
    dotenv -f .env run -- python dead_letter_exchange/failed_consume.py
```

## Notes

1. [Pika client](https://pika.readthedocs.io/en/stable/)