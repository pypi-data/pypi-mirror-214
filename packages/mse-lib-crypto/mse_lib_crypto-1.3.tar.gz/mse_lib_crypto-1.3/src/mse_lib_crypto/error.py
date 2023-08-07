"""mse_lib_crypto.error module."""


class NonceNotFound(Exception):
    """Error when nonce does not exist for a specific path."""


class ExtensionNotFound(Exception):
    """Error when suffix extension is not found in a specific path."""
