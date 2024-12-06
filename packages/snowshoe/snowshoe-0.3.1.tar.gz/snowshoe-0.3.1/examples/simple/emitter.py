from time import time, sleep

from src.snowshoe import Snowshoe

app = Snowshoe(
    name='emitter_1',
    host='127.0.0.1',
    port=5672,
    username='rabbit',
    password='rabbit',
)

app.run(False)

for i in range(100):
    app.emit('hello', {'now': time(), 'i': i})
    sleep(10)
    # break

sleep(5)