import traceback


class GetSecretException(Exception):
    """Raised when a secret store operation fails."""

    def __init__(self, inner_exception: Exception, secret_key: str):
        message = f"Failed to get secret with key: {secret_key}. Secret store exception:\n{''.join(traceback.format_exception(inner_exception))}"
        super().__init__(message)


class PutSecretException(Exception):
    """Raised when a secret store operation fails."""

    def __init__(self, inner_exception: Exception):
        message = f"Failed to put secret. Secret store exception:\n{''.join(traceback.format_exception(inner_exception))}"
        super().__init__(message)
