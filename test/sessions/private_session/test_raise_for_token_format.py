"""Module to test the is_valid_token_format"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.sessions.private_session import (
    PrivateSession,
    HomeAssistant,
    ConfigEntry,
    TokenRefreshError,
)


class TestValidFormat(TestCase):

    def test_proper_lenght_token(self):

        token = "".join(["a"]*PrivateSession.TOKEN_LENGTH)

        mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        session = PrivateSession(mocks["hass"], mocks["entry"])

        session.raise_for_invalid_token(token, "foo")


class TestInvalidFormat(TestCase):

    def test_improper_lenght_token(self):

        token = "".join(["a"]*(PrivateSession.TOKEN_LENGTH-10))

        mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "entry": MagicMock(spec=ConfigEntry)
        }

        mocks["entry"].data = {
            "internal_api": {
                "sp_dc": "foo",
                "sp_key": "bar",
            }
        }

        session = PrivateSession(mocks["hass"], mocks["entry"])

        with self.assertRaises(TokenRefreshError):
            session.raise_for_invalid_token(token, "foo")
