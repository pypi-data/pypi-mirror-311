""" Routing keys for messages. """

import enum


class RoutingKeys(enum.StrEnum):
    """Broadcast keys."""

    NOTIFICATION = "messaging.evilcouncil.notification"
    HTTP_LOG_COLLECTION = "infra.log_collect.http"
    DOCKER_LOG_COLLECTION = "infra.log_collect.docker"
    MALWARE_URLS = "infra.malware.urls"


class ConsumerKeys(enum.StrEnum):
    """Consumer keys."""

    INFRA_ALL = "infra.#"
    INFRA_LOG_COLLECT = "infra.log_collect.#"
    MALARE_URLS = "infra.malware.urls"
