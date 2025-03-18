"""Module to test the raise for status function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch
import json

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    HomeAssistant,
    ConfigEntry,
    InternalServerError,
    ExpiredSpotifyCookiesError,
    TokenRefreshError
)


class TestInternalServerError(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

    def test_error_raised(self):
        with self.assertRaises(InternalServerError):
            self.session.raise_for_status(502, "foo", {})

    def test_set_unhealthy(self):
        try:
            self.session.raise_for_status(502, "foo", {})
        except InternalServerError:
            pass

        self.assertFalse(self.session._is_healthy)


class TestExpiredCookieError(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

    def test_error_raised(self):
        with self.assertRaises(ExpiredSpotifyCookiesError):
            self.session.raise_for_status(
                302,
                "foo",
                {"Location": self.session.EXPIRED_LOCATION}
            )

    def test_set_unhealthy(self):
        try:
            self.session.raise_for_status(
                302,
                "foo",
                {"Location": self.session.EXPIRED_LOCATION}
            )
        except ExpiredSpotifyCookiesError:
            pass

        self.assertFalse(self.session._is_healthy)


class TestTokenRefreshError(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

    def test_error_raised(self):
        with self.assertRaises(TokenRefreshError):
            self.session.raise_for_status(
                200,
                "foo",
                {"Location": self.session.EXPIRED_LOCATION}
            )

    def test_set_unhealthy(self):
        try:
            self.session.raise_for_status(
                200,
                "foo",
                {"Location": self.session.EXPIRED_LOCATION}
            )
        except TokenRefreshError:
            pass

        self.assertFalse(self.session._is_healthy)


class TestValidResponse(TestCase):

    def setUp(self):

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        self.mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        self.session = PrivateSession(self.mocks["hass"], self.mocks["entry"])

    def test_no_error_raised(self):

        content = json.dumps({
            "accessToken": "".join(["a"]*PrivateSession.TOKEN_LENGTH)
        })

        try:
            self.session.raise_for_status(200, content, {})
        except (
                TokenRefreshError,
                ExpiredSpotifyCookiesError,
                InternalServerError,
        ) as exc:
            self.fail(exc)
