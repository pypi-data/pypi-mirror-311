import random
from threading import Thread
from time import sleep

from src.snowshoe import snowshoe

app = snowshoe.Snowshoe(
    name='consumer_1',
    host='127.0.0.1',
    port=5672,
    username='rabbit',
    password='rabbit',
    concurrency=1
)

app.define_queues([
    snowshoe.Queue(
        name='my_queue',
        bindings=[snowshoe.QueueBinding('emitter_1', 'hello')],
        failure_method=snowshoe.FailureMethod.DLX,
        durable=False,
        consumer_timeout=1000,
        auto_delete=True
    ),
])


@app.on('my_queue')
def queue_message_handler(message: snowshoe.Message):
    print(message.topic, message.data, message.delivery_tag, message.id)
    # raise Exception(':#')
    sleep(random.uniform(5, 10))


def print_status():
    while True:
        print(app.status)
        sleep(10)


# Thread(target=print_status).start()

app.run(True)
