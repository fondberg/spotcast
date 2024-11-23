"""Module to test the async_play_saved_episodes function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.play_saved_episodes import (
    async_play_saved_episodes,
    HomeAssistant,
    ServiceCall,
    SpotifyAccount,
)

TEST_MODULE = "custom_components.spotcast.services.play_saved_episodes"


class TestServiceCall(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.async_play_custom_context")
    @patch.object(SpotifyAccount, "async_from_config_entry")
    async def asyncSetUp(
            self,
            mock_account: AsyncMock,
            mock_play: AsyncMock,
            mock_entries: MagicMock,
    ):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
            "play": mock_play,
            "entries": mock_entries
        }

        self.mocks["call"].data = {
            "media_player": {
                "entity_id": [
                    "media_player.foo"
                ]
            }
        }
        self.mocks["account"].async_saved_episodes = AsyncMock()
        self.mocks["account"].async_saved_episodes\
            .return_value = [
                {"episode": {"uri": "foo"}},
                {"episode": {"uri": "bar"}},
                {"episode": {"uri": "baz"}},
        ]
        self.mocks["entries"].return_value = "foo"

        await async_play_saved_episodes(self.mocks["hass"], self.mocks["call"])

    def test_play_custom_context_properly_called(self):
        try:
            self.mocks["play"].assert_called_with(
                self.mocks["hass"],
                self.mocks["call"],
            )
        except AssertionError:
            self.fail()

    def test_call_data_properly_modified(self):
        self.assertEqual(
            self.mocks["call"].data,
            {
                "media_player": {
                    "entity_id": [
                        "media_player.foo"
                    ]
                },
                "tracks": ["foo", "bar", "baz"]
            }
        )
