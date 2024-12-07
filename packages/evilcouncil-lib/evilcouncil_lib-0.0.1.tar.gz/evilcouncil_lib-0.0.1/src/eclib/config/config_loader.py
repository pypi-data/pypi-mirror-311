""" Provide abstract base class for loading configs."""

import abc
from . import config_constants


# pylint: disable=too-few-public-methods
class ConfigLoader(abc.ABC):
    """Load configs"""

    def get_config(self, key: config_constants.ConfigConstants):
        """get vaalue"""
