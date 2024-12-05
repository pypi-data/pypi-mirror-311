import json
import logging

from sqlalchemy import types

from mind_castle.stores import get_secret, put_secret
from mind_castle.exceptions import PutSecretException

logger = logging.getLogger(__name__)
logger.level = logging.DEBUG


class SecretData(types.TypeDecorator):
    """A sqlalchemy field type that stores data in a secret store."""

    impl = types.JSON  # The base data type for this field
    cache_ok = True

    def __init__(self, store_type: str, secret_key_prefix: str = "", *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.secret_type = store_type
        self.secret_key_prefix = secret_key_prefix

    def process_bind_param(self, value, dialect):
        """Convert a plaintext value into a secret and return it to be stored."""
        # Don't waste time storing empty values
        if value is None or value == "" or value == {} or value == []:
            return value

        # Make a string out of whatever object we got
        stringValue = json.dumps(value)

        try:
            secret_params = put_secret(stringValue, self.secret_type)
            logger.debug(f"Stored secret with: {secret_params}")
        except PutSecretException as e:
            logger.error(
                f"Failed to store secret in {self.secret_type}. Falling back to plaintext."
            )
            logger.error(e)

            secret_params = put_secret(stringValue, "plaintext")
            logger.warning(f"Stored secret IN PLAINTEXT with: {secret_params}")

        return secret_params

    def process_result_value(self, value, dialect):
        """Convert a secret from the DB into the original value."""

        if value is None:
            return None

        # Get a dict of the secret details
        secret_details = json.loads(value) if isinstance(value, str) else value

        # This might be an old plaintext value
        if secret_details.get("mind_castle_secret_type") is None:
            logger.debug(
                f"No secret type found in '{secret_details}', must be a plaintext value."
            )
            return secret_details

        logger.debug(f"Restoring {secret_details} from a secret.")
        return json.loads(get_secret(secret_details))
