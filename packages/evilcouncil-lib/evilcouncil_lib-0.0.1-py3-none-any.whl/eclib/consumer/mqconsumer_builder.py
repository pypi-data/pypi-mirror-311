""" Build an mqconsumer"""

import queue

from . import mqconsumer
from ..config import config_constants
from ..config import config_loader
from ..msg import routing_keys


def build_mq_consumer(
    cl: config_loader.ConfigLoader, ck: routing_keys.ConsumerKeys
) -> mqconsumer.MQConsumer:
    """Builds mq consumer"""
    server = cl.get_config(config_constants.ConfigConstants.RABBIT_SERVER)
    port = cl.get_config(config_constants.ConfigConstants.RABBIT_PORT)
    exchange = cl.get_config(config_constants.ConfigConstants.RABBIT_EXCHANGE)
    local_queue = queue.Queue()

    return mqconsumer.MQConsumer(server, port, exchange, ck, local_queue)
