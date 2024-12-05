import logging

from mind_castle.secret_store_base import SecretStoreBase

logger = logging.getLogger(__name__)


# DO NOT USE THIS STORE IN PRODUCTION
# It will store your secrets IN PLAIN TEXT in memory and
# they will be lost when the application is restarted


class MemorySecretStore(SecretStoreBase):
    """
    An in-memory secret store.
    This is not persistent and will be lost when the application is restarted.
    Use only for testing or development.
    """

    store_type = "memory"

    def __init__(self):
        self.secrets = {}

    def get_secret(self, secret_details: dict) -> str:
        key = secret_details.get("key")
        return self.secrets.get(key)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        self.secrets[key] = value
        return {"mind_castle_secret_type": self.store_type, "key": key}
