""" Build an MQ Publisher."""

from . import mqpublisher
from ..config import config_constants
from ..config import config_loader


def build_mq_publisher(cl: config_loader.ConfigLoader) -> mqpublisher.MQPublisher:
    """Build an MQ Publisher"""
    server = cl.get_config(config_constants.ConfigConstants.RABBIT_SERVER)
    port = cl.get_config(config_constants.ConfigConstants.RABBIT_PORT)
    exchange = cl.get_config(config_constants.ConfigConstants.RABBIT_EXCHANGE)

    return mqpublisher.MQPublisher(host=server, port=port, exchange=exchange)
