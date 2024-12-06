import os

import hvac
from hvac.exceptions import VaultError

from mind_castle.secret_store_base import SecretStoreBase
from mind_castle.exceptions import GetSecretException, PutSecretException


class HashiCorpVaultSecretStore(SecretStoreBase):
    """
    Uses HashiCorp Vault to store secrets.
    """

    store_type = "hashicorpvault"
    required_config = [["MIND_CASTLE_VAULT_HOST", "MIND_CASTLE_VAULT_TOKEN"]]

    def __init__(self):
        self.client = hvac.Client(
            url=os.environ.get("MIND_CASTLE_VAULT_HOST"),
            token=os.environ.get("MIND_CASTLE_VAULT_TOKEN"),
        )
        self.mount_point = "cubbyhole/"

    def get_secret(self, secret_details: dict) -> str:
        key = secret_details.get("key")
        try:
            response = self.client.secrets.kv.v1.read_secret(
                path=key, mount_point=self.mount_point
            )
        except VaultError as e:
            raise GetSecretException(e, key)

        return response["data"]["data"].get("secret_value")

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        try:
            self.client.secrets.kv.v1.create_or_update_secret(
                path=key, secret=dict(secret_value=value), mount_point=self.mount_point
            )  # Value has to be a dict so just make a 'secret_value' key
        except VaultError as e:
            raise PutSecretException(e, key)

        return {"mind_castle_secret_type": self.store_type, "key": key}
