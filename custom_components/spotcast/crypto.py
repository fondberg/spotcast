"""Module for cryptographic methods and functions"""

from base64 import b32encode

from pyotp import TOTP


_CIPHER_BASE = (12, 56, 76, 33, 88, 44, 88, 33,
                78, 78, 11, 66, 22, 22, 55, 69, 54)
CIPHER_BYTES = [j ^ (i % 33 + 9) for i, j in enumerate(_CIPHER_BASE)]


def hex_to_bytes(data: str) -> bytes:
    """Converts a hex string to bytes"""
    data = data.replace(" ", "")
    return bytes.fromhex(data)


def get_totp(
        digits: int = 6,
        digest: str = "sha1",
        interval: int = 30
) -> TOTP:
    """Provides a time-based OTP manager compliant for spotify TOTP
    scheme"""

    secret_hex = ''.join(str(x) for x in CIPHER_BYTES)
    secret_hex = secret_hex.encode()
    secret_hex = "".join(format(x, 'x') for x in secret_hex)
    secret_bytes = hex_to_bytes(secret_hex)
    secret = b32encode(secret_bytes).decode().strip('=')

    return TOTP(secret, digits=digits, digest=digest, interval=interval)
