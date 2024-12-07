"""Download yaml file for config parsing."""

import requests
import yaml

from . import config_loader
from . import config_constants


# pylint: disable=too-few-public-methods
class HttpYamlConfigLoader(config_loader.ConfigLoader):
    """Download yaml configs for parsing."""

    def __init__(self, config_url: str):
        response = requests.get(config_url, timeout=10)
        response.raise_for_status()
        self._data = yaml.safe_load(response.text)

    def get_config(self, key: config_constants.ConfigConstants):
        data = self._data
        for kp in key.split("."):
            val = data.get(kp, None)
            if val is None:
                raise ValueError

            if isinstance(val, dict):
                data = val
            else:
                return val

        raise ValueError
