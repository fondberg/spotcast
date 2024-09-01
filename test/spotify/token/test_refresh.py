"""Module to test the refresh method"""

from unittest import TestCase
from unittest.mock import patch, MagicMock
from time import time
import json

from requests import HTTPError

from custom_components.spotcast.spotify.token import (
    SpotifyToken,
    Session,
    ExpiredCookiesError,
    InvalidCookiesError,
    UnknownTokenError,
)


class TestTokenRefresh(TestCase):

    def setUp(self):
        self.token = SpotifyToken("12345", time() + 1000)

    @patch.object(Session, "get")
    def test_token_gets_refreshed(self, mock_get: MagicMock):

        mock_get.return_value.json.return_value = {
            "clientId": "12345",
            "accessToken": "67890",
            "accessTokenExpirationTimestampMs": 1234567890
        }

        token, expires = self.token._refresh(sp_dc="foo", sp_key="bar")

        self.assertEqual(token, "67890")
        self.assertEqual(expires, 1234567.89)


class TestErrors(TestCase):

    def setUp(self):
        self.token = SpotifyToken("12345", time() + 1000)
        return
        with open("./config/spotify_tokens.json") as file:
            self.config = json.load(file)

    @patch.object(Session, "get")
    def test_invalid_cookies(self, mock_get: MagicMock):

        mock_get.return_value.status_code = 401
        mock_get.return_value.raise_for_status.side_effect = HTTPError()

        with self.assertRaises(InvalidCookiesError):
            self.token._refresh("foo", "bar")

    # TODO: revist once spotify had time to expire the token
    def test_expired_cookies(self):

        return

        with self.assertRaises(ExpiredCookiesError):
            self.token._refresh(**self.config)

    @patch.object(Session, "get")
    def test_unexpected_error_code(self, mock_get: MagicMock):

        mock_get.return_value.status_code = 500
        mock_get.return_value.raise_for_status.side_effect = HTTPError()

        with self.assertRaises(UnknownTokenError):
            self.token._refresh("foo", "bar")

    @patch.object(Session, "get")
    def test_unexpected_data_in_response(self, mock_get: MagicMock):

        mock_get.return_value.json.return_value = {
            "foo": "bar"
        }

        with self.assertRaises(UnknownTokenError):
            self.token._refresh("foo", "bar")
