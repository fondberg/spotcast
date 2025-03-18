"""Module with utility functions for cryptographic functions

Functions:
    - hex_to_bytes
"""


def hex_to_bytes(data: str) -> bytes:
    """Converts a hex string to bytes"""
    data = data.replace(" ", "")
    return bytes.fromhex(data)
