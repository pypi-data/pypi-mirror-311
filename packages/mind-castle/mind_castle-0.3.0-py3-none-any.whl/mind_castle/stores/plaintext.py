import logging

from mind_castle.secret_store_base import SecretStoreBase

logger = logging.getLogger(__name__)


# DO NOT USE THIS STORE IN PRODUCTION
# It will store your secrets IN PLAIN TEXT in the DB


class PlaintextSecretStore(SecretStoreBase):
    """
    A nop secret store that just stores the given plaintext in the DB.
    Use only for testing or development.
    """

    store_type = "plaintext"

    def get_secret(self, secret_details: dict) -> str:
        return secret_details.get("key")

    def put_secret(self, value: str) -> dict:
        return {"mind_castle_secret_type": self.store_type, "key": value}
