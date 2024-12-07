""" Default message class. """

import dataclasses
import json

from . import routing_keys
from . import message


@dataclasses.dataclass
class Notification(message.Message):
    """Provide notification messages."""

    msg: str

    def get_message(self) -> str:
        return json.dumps({"message": self.msg})

    def get_routing_key(self) -> routing_keys.RoutingKeys:
        return routing_keys.RoutingKeys.NOTIFICATION
