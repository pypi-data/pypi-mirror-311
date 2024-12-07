""" Provide constants for loading configs."""

import enum


class ConfigConstants(enum.StrEnum):
    """Config variables."""

    RABBIT_SERVER = "rabbit.server"
    RABBIT_PORT = "rabbit.port"
    RABBIT_EXCHANGE = "rabbit.exchange"
    RABBIT_QUEUE = "rabbit.queue"
    MYSQL_SERVER = "mysql.server"
    MYSQL_PORT = "mysql.port"
    MYSQL_USER = "mysql.user"
    MYSQL_PASSWORD = "mysql.password"
