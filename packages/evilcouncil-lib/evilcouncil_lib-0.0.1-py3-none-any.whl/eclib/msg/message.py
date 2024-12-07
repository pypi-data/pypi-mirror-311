""" Base class for messages. """

import abc


from . import routing_keys


class Message(abc.ABC):
    """Base message class."""

    def get_message(self) -> str:
        """Gets JSON string of message"""

    def get_routing_key(self) -> routing_keys.RoutingKeys:
        """Gets routing key for message"""
