"""Module to test the get_profile_value function"""

from unittest import TestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    HomeAssistant,
    OAuth2Session,
    InternalSession,
    ProfileNotLoadedError,
)


class TestProfileLoaded(TestCase):

    def setUp(self):

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

        self.account._profile = {
            "foo": "bar",
            "hello": "world"
        }

    def test_value_retrieval(self):
        self.assertEqual(self.account.get_profile_value("foo"), "bar")

    def test_non_existing_value_returns_none(self):
        self.assertIsNone(self.account.get_profile_value("boo"))


class TestProfileNotLoaded(TestCase):

    def setUp(self):

        self.account = SpotifyAccount(
            MagicMock(spec=HomeAssistant),
            MagicMock(spec=OAuth2Session),
            MagicMock(spec=InternalSession),
        )

    def test_raises_error(self):
        with self.assertRaises(ProfileNotLoadedError):
            self.account.get_profile_value("foo")
