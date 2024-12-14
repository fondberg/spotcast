"""Module to test the async_like_media function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, AsyncMock, patch

from custom_components.spotcast.services.like_media import (
    async_like_media,
    SpotifyAccount,
    ServiceCall,
    HomeAssistant,
)

from test.services.like_media import TEST_MODULE


class TestLikingMedia(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_from_config_entry")
    @patch(f"{TEST_MODULE}.get_account_entry", new_callable=MagicMock)
    async def asyncSetUp(self, mock_entry: MagicMock, mock_account: AsyncMock):

        mock_account.return_value = MagicMock(spec=SpotifyAccount)

        self.mocks = {
            "hass": MagicMock(spec=HomeAssistant),
            "call": MagicMock(spec=ServiceCall),
            "account": mock_account.return_value,
        }

        self.mocks["account"].async_like_media = AsyncMock()

        self.mocks["call"].data = {
            "spotify_uris": ["foo", "bar", "baz"]
        }

        await async_like_media(self.mocks["hass"], self.mocks["call"])

    def test_like_media_properly_called(self):
        try:
            self.mocks["account"].async_like_media.assert_called_with(
                ["foo", "bar", "baz"]
            )
        except AssertionError:
            self.fail()
