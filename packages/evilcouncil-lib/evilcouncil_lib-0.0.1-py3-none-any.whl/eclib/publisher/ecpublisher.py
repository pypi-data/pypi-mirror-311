""" Base class for """

import abc
from ..msg import message


# pylint: disable=too-few-public-methods
class ECPublisher(abc.ABC):
    """Base class for EC publishers."""

    def send_message(self, msg: message.Message):
        """Sends message to appropirate destination."""
