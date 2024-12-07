"""Read from rabbitmq, dump data onto a queue"""

import json
import time
import threading

# rabbitmq
import pika


from ..msg import routing_keys


# pylint: disable=too-many-instance-attributes
class MQConsumer(threading.Thread):
    """Object to wrap around RabbitMQ and send gelf data"""

    # pylint: disable=too-many-arguments
    # pylint: disable=too-many-positional-arguments
    def __init__(
        self,
        host: str,
        port: int,
        exchange: str,
        routes: routing_keys.ConsumerKeys,
        local_queue: queue.Queue,
    ):
        super().__init__()
        self._exchange = exchange
        self._routing_key = routes
        self._host = host
        self._port = port
        self._running = True
        self._queue = local_queue
        self._queue_name = None
        self._rabbitqueue = None
        self._channel = None
        self._connection = None

    def _connect(self):
        # why did i turn heartbeat off
        # self.conection = pika.BlockingConnection(
        # pika.ConnectionParameters(host=self.host, port=self.port, heartbeat=0))
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self._host, port=self._port)
        )
        self._channel = self._connection.channel()
        self._channel.exchange_declare(
            exchange=self._exchange, exchange_type="topic", durable=True
        )

        self._rabbitqueue = self._channel.queue_declare(
            "", auto_delete=True, exclusive=True
        )
        self._queue_name = self._rabbitqueue.method.queue
        self._channel.queue_bind(
            exchange=self._exchange,
            queue=self._queue_name,
            routing_key=self._routing_key,
        )

    def run(self):
        self._connect()
        self._channel.basic_consume(self._queue_name, self.handle_message)

        while self._running:
            time.sleep(1)
            self._connection.process_data_events()

            #     self.conection.process_data_events()

        self._connection.close()

    def stop(self):
        """Stop doing the thing."""
        self._running = False

    # pylint: disable=unused-argument
    def handle_message(self, channel, method_frame, header_frame, body):
        """Process incoming message."""
        # print(method_frame.delivery_tag)
        self._queue.put_nowait(json.loads(body))
        # channel.basic_ack(delivery_tag=header_frame.delivery_tag)

    @property
    def queue(self) -> queue.Queue:
        """Get the current queue object"""
        return self._queue
