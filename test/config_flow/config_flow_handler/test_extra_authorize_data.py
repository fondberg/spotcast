"""Module to test the extra_authorize_data property"""

from unittest import TestCase

from custom_components.spotcast.spotify import SpotifyAccount
from custom_components.spotcast.config_flow.config_flow_handler import (
    SpotcastFlowHandler
)


class TestScopeValue(TestCase):

    def setUp(self):
        self.flow_handler = SpotcastFlowHandler()

    def test_property_returns_dictionary(self):
        self.assertIsInstance(self.flow_handler.extra_authorize_data, dict)

    def test_property_contain_scope_as_key(self):
        self.assertIn("scope", self.flow_handler.extra_authorize_data)

    def test_scope_is_set_to_spotcast_spotify_scope(self):
        self.assertEqual(
            self.flow_handler.extra_authorize_data["scope"].split(","),
            list(SpotifyAccount.SCOPE)
        )
