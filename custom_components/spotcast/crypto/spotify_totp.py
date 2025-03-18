"""Module for managing spotify time-based one time password"""

from base64 import b32encode

from pyotp import TOTP
from custom_components.spotcast.crypto.utils import hex_to_bytes


_CIPHER_BASE = (12, 56, 76, 33, 88, 44, 88, 33,
                78, 78, 11, 66, 22, 22, 55, 69, 54)
CIPHER_BYTES = [j ^ (i % 33 + 9) for i, j in enumerate(_CIPHER_BASE)]


def get_totp(
        digits: int = 6,
        digest: str = "sha1",
        interval: int = 30
) -> TOTP:
    """Provides a time-based OTP manager compliant for spotify TOTP
    scheme"""

    secret_hex = ''.join(f"{x:02x}" for x in CIPHER_BYTES)
    secret_bytes = hex_to_bytes(secret_hex)
    secret = b32encode(secret_bytes).decode().strip('=')

    return TOTP(secret, digits=digits, digest=digest, interval=interval)
