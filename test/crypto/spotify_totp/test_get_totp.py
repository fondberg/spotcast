"""Module to test the get_totp_function"""

from unittest import TestCase
from base64 import b32encode

from custom_components.spotcast.crypto.spotify_totp import (
    get_totp,
    CIPHER_BYTES,
    hex_to_bytes,
    TOTP,
)


class TestTotpCreation(TestCase):

    def setUp(self):

        self.totp = get_totp()
        secret_hex = ''.join(str(x) for x in CIPHER_BYTES)
        secret_hex = secret_hex.encode()
        secret_hex = "".join(format(x, 'x') for x in secret_hex)
        secret_bytes = hex_to_bytes(secret_hex)
        self.expected_secret = b32encode(secret_bytes).decode().strip('=')

    def test_totp_object_provided(self):
        self.assertIsInstance(self.totp, TOTP)

    def test_proper_secret_created(self):
        self.assertEqual(self.expected_secret, self.totp.secret)

    def test_digits_size_properly_set(self):
        self.assertEqual(self.totp.digits, 6)

    def test_interval_set(self):
        self.assertEqual(self.totp.interval, 30)

    def test_digest_set(self):
        self.assertEqual(self.totp.digest, "sha1")
