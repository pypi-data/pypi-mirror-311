""" Publish events on MQ."""

import pika

from ..msg import message
from . import ecpublisher


# pylint: disable=too-few-public-methods
class MQPublisher(ecpublisher.ECPublisher):
    """Publish messages on MQ."""

    def __init__(self, host: str, port: int, exchange: str):
        self._conn_param = pika.ConnectionParameters(host=host, port=port)
        self._exchange = exchange

    def send_message(self, msg: message.Message):
        with pika.BlockingConnection(self._conn_param) as conn:
            channel = conn.channel()

            channel.basic_publish(
                exchange=self._exchange,
                routing_key=msg.get_routing_key(),
                body=msg.get_message(),
            )
