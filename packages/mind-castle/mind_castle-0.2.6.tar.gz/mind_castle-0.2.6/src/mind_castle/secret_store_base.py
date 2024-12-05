import uuid
from abc import ABC, abstractmethod


class SecretStoreBase(ABC):
    """This is an abstract class that defines the interface for a secret store."""

    store_type = "base"
    required_config = [[]]
    optional_config = []

    @abstractmethod
    def get_secret(self, secret_details: dict) -> str:
        raise NotImplementedError()

    @abstractmethod
    def put_secret(self, value: str) -> dict:
        raise NotImplementedError()

    def get_secret_key(self) -> str:
        """
        Generates a key based on this machine's hardware and the time.
        https://docs.python.org/3/library/uuid.html#uuid.uuid1
        """

        return str(uuid.uuid1())
