"""Module to test the constructor of the SpotifyToken Class"""

from unittest import TestCase
from time import time
from unittest.mock import patch, MagicMock

from custom_components.spotcast.spotify.token import SpotifyToken


class TestNotExpiredToken(TestCase):

    @patch.object(SpotifyToken, "get")
    def test_construction_doesnt_call_refresh(self, mock_get: MagicMock):

        expires = time() + 1000

        SpotifyToken("12345", expires)

        try:
            mock_get.assert_not_called()
        except AssertionError:
            self.fail("_refresh method was called")

    def test_construction_retains_provided_token(self):

        expires = time() + 1000
        token = SpotifyToken("12345", expires)

        self.assertEqual(token._access_token, "12345")


class TestNoTokenProvided(TestCase):

    @patch.object(SpotifyToken, "get")
    def test_in_absence_of_token_a_new_token_is_fetched(
            self,
            mock_get: MagicMock
    ):

        SpotifyToken(sp_dc="12345", sp_key="67890")

        try:
            mock_get.assert_called_once()
        except AssertionError:
            if mock_get.call_count == 0:
                self.fail("get was never called")
            else:
                self.fail("get was called more than once")

    def test_missing_sp_dc_causes_error(self):

        with self.assertRaises(TypeError):
            SpotifyToken(sp_key="67890")

    def test_missing_sp_key_causes_error(self):

        with self.assertRaises(TypeError):
            SpotifyToken(sp_dc="12345")


class TestExpiredToken(TestCase):

    @patch.object(SpotifyToken, "get")
    def test_in_absence_of_token_a_new_token_is_fetched(
            self,
            mock_get: MagicMock
    ):

        expires = time() - 1000

        SpotifyToken(
            access_token="foo",
            expires=expires,
            sp_dc="12345",
            sp_key="67890",
        )

        try:
            mock_get.assert_called_once()
        except AssertionError:
            if mock_get.call_count == 0:
                self.fail("get was never called")
            else:
                self.fail("get was called more than once")
