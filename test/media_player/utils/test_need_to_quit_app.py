"""Modulew to test the need to quit app function"""

from unittest import TestCase
from unittest.mock import MagicMock

from custom_components.spotcast.media_player.utils import (
    need_to_quit_app,
    Chromecast,
    SpotifyAccount,
)


class TestTueCases(TestCase):

    def setUp(self):

        self.mocks = {
            "media_player": MagicMock(spec=Chromecast),
            "account": MagicMock(spec=SpotifyAccount)
        }

    def run_test(self):
        self.assertTrue(need_to_quit_app(
            media_player=self.mocks["media_player"],
            account=self.mocks["account"],
            app_id="foo"
        ))

    def test_running_spotify_but_not_account_active_device(self):

        self.mocks["media_player"].app_id = "foo"
        self.mocks["media_player"].id = "bar"
        self.mocks["account"].active_device = "baz"

        self.run_test()

    def test_media_player_running_different_app(self):

        self.mocks["media_player"].app_id = "far"
        self.mocks["media_player"].id = "bar"
        self.mocks["account"].active_device = "baz"

        self.run_test()


class TestFalseCases(TestCase):

    def setUp(self):

        self.mocks = {
            "media_player": MagicMock(spec=Chromecast),
            "account": MagicMock(spec=SpotifyAccount)
        }

    def run_test(self):
        self.assertFalse(need_to_quit_app(
            media_player=self.mocks["media_player"],
            account=self.mocks["account"],
            app_id="foo"
        ))

    def test_no_active_app(self):

        self.mocks["media_player"].app_id = None
        self.mocks["media_player"].id = "bar"
        self.mocks["account"].active_device = "baz"

        self.run_test()

    def test_media_player_active_for_account(self):

        self.mocks["media_player"].app_id = "foo"
        self.mocks["media_player"].id = "bar"
        self.mocks["account"].active_device = "bar"

        self.run_test()
