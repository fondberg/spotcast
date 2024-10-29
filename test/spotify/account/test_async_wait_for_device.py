"""Module to test the async_wait_for_device function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    OAuth2Session,
    InternalSession,
    HomeAssistant,
)

from test.unit_utils import AsyncMock


class TestDeviceBecomesAvailable(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_devices", new_callable=AsyncMock)
    async def test_function_returns(self, mock_devices: MagicMock):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.account = SpotifyAccount(
            hass=mock_hass,
            internal_session=mock_internal,
            external_session=mock_external,
        )

        mock_devices.side_effect = [
            [{"id": "bar"}],
            [{"id": "bar"}, {"id": "foo"}],
        ]

        try:
            await self.account.async_wait_for_device("foo")
        except TimeoutError:
            self.fail("function failed to get device before timeout")


class TestFunctionTimesOut(IsolatedAsyncioTestCase):

    @patch.object(SpotifyAccount, "async_devices", new_callable=AsyncMock)
    async def test_function_raises(self, mock_devices: MagicMock):

        mock_hass = MagicMock(spec=HomeAssistant)
        mock_internal = MagicMock(spec=InternalSession)
        mock_external = MagicMock(spec=OAuth2Session)

        self.account = SpotifyAccount(
            hass=mock_hass,
            internal_session=mock_internal,
            external_session=mock_external,
        )

        mock_devices.return_value = [
            {"id": "bar"},
        ]

        with self.assertRaises(TimeoutError):
            await self.account.async_wait_for_device("foo", timeout=1)
