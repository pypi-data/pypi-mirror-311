import glob
import logging
import os
from os.path import basename, dirname, isfile, join

from mind_castle.secret_store_base import SecretStoreBase

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [
    basename(f)[:-3] for f in modules if isfile(f) and not f.endswith("__init__.py")
]

from . import *  # noqa: F401, F403, E402, isort:skip

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG

# Get all env vars with our prefix
env_vars = {k: v for k, v in os.environ.items() if k.startswith("MIND_CASTLE_")}

stores = {}

# Populate 'stores' dict with instantiated stores
for subclass in SecretStoreBase.__subclasses__():
    configured = False
    for config_set in subclass.required_config:
        if all(e in env_vars.keys() for e in config_set):
            stores[subclass.store_type] = subclass()
            secret_store = subclass()
            logger.debug(f"Configured secret store '{subclass.store_type}'")
            configured = True

        elif not configured and any(e in env_vars.keys() for e in config_set):
            # Log a warning if some but not all required config is present
            logger.warning(
                f"Missing required config for store '{subclass.store_type}'. Requires: {config_set}"
            )


def get_secret(data: dict) -> str:
    secret_type = data.get("mind_castle_secret_type")
    if secret_type is None:
        raise ValueError("No mind_castle_secret_type provided in data")

    secret_store = stores.get(secret_type)
    if secret_store is None:
        raise ValueError(
            f"Trying to retrieve secret from unknown/unconfigured store '{secret_type}'"
        )
    # TODO: handle 'key' key missing
    return secret_store.get_secret(data)


def put_secret(value: str, secret_type: str) -> dict:
    secret_store = stores.get(secret_type)
    if secret_store is None:
        raise ValueError(
            f"Trying to put secret to unknown/unconfigured store '{secret_type}'"
        )

    return secret_store.put_secret(value)
