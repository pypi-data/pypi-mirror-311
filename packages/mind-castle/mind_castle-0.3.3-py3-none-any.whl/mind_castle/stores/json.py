import json
import logging
import os

from mind_castle.secret_store_base import SecretStoreBase

logger = logging.getLogger(__name__)

# DO NOT USE THIS STORE IN PRODUCTION
# It will store your secrets IN PLAIN TEXT in a JSON file


class JsonSecretStore(SecretStoreBase):
    store_type = "json"
    filename = "secrets.json"

    def __init__(self):
        if not os.path.exists(self.filename):
            with open(self.filename, "w") as f:
                f.write("{}")

    def get_secret(self, secret_details: dict) -> str:
        key = secret_details.get("key")
        with open(self.filename, "r") as f:
            secrets = json.load(f)
        return secrets.get(key)

    def put_secret(self, value: str) -> dict:
        key = self.get_secret_key()
        with open(self.filename, "r") as f:
            secrets = json.load(f)
            secrets[key] = value

        with open(self.filename, "w") as f:
            json.dump(secrets, f)
        return {"mind_castle_secret_type": self.store_type, "key": key}
