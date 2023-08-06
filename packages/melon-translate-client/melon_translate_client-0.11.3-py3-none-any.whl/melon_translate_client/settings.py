import logging

from decouple import config

# NOTE: Logging configuration
log = logging.getLogger("melon_translate_client")

# NOTE: Mandatory settings
TRANSLATE_URL = config(
    "TRANSLATE_URL", default="https://translate.dev.getmelon.dev"
)

# NOTE: Optional settings
TRANSLATE_ENABLED = config("TRANSLATE_ENABLED", default=False, cast=bool)
TRANSLATE_REQUESTS_TIMEOUT = config("TRANSLATE_REQUESTS_TIMEOUT", default=30, cast=int)
TRANSLATE_CACHE_VIEW_TTL = config("TRANSLATE_CACHE_VIEW_TTL", default=300, cast=int)
TRANSLATE_TTL_JITTER = config("TRANSLATE_TTL_JITTER", default=300, cast=int)

# NOTE: This is the number of worker threads that will be spawned to process translation requests.
# To calculate exact number of threads that will be spawned when size is `0` on Kubernetes we have
# to look at the K8S limits for the container in which we spawn the worker. If there is no limit, the
# container will see the host node CPU count and use following formula to calculate the number of threads:
#  `cpu_count + 4` - for both IO and CPU bound tasks which release GIL.
TRANSLATE_WORKER_POOL_SIZE = config("TRANSLATE_WORKER_POOL_SIZE", default=0, cast=int)
