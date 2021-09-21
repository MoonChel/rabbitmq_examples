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


### Plan and execute tasks in future

![Image of Yaktocat](https://github.com/MoonChel/rabbitmq_examples/blob/adf68311e03ad7f74a6823ca1bc761dc89f719b7/images/task_planning_for_future.png)

## Notes

1. [Pika client](https://pika.readthedocs.io/en/stable/)