"""Module to test the async_relay_service_call"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import MagicMock, patch, AsyncMock

from urllib3.exceptions import ReadTimeoutError

from custom_components.spotcast.services.service_handler import (
    ServiceHandler,
    HomeAssistant,
    ServiceCall,
    UnknownServiceError,
    SERVICE_HANDLERS
)

TEST_MODULE = "custom_components.spotcast.services.service_handler"


class TestServiceCall(IsolatedAsyncioTestCase):

    @patch(f"{TEST_MODULE}.SERVICE_HANDLERS", new_callable=MagicMock)
    async def asyncSetUp(self, mock_handlers: MagicMock):

        self.mock_play_media = AsyncMock()

        self.mock_handlers = mock_handlers
        self.mock_handlers.__getitem__.return_value = self.mock_play_media
        self.hass = MagicMock(spec=HomeAssistant)
        self.call = MagicMock(spec=ServiceCall)
        self.call.service = "play_media"

        handler = ServiceHandler(self.hass)

        await handler.async_relay_service_call(self.call)

    async def test_async_play_media_was_called(self):
        try:
            self.mock_play_media.assert_called()
        except AssertionError:
            self.fail()

    async def test_async_play_received_hass_and_call(self):
        try:
            self.mock_play_media.assert_called_with(
                self.hass,
                self.call,
            )
        except AssertionError:
            self.fail()


class TestUnknownService(IsolatedAsyncioTestCase):

    async def test_error_raised(self):

        self.hass = MagicMock(spec=HomeAssistant)
        self.call = MagicMock(spec=ServiceCall)
        self.call.service = "unkown_service"

        handler = ServiceHandler(self.hass)

        with self.assertRaises(UnknownServiceError):
            await handler.async_relay_service_call(self.call)


class TestErrorDuringServiceCall(IsolatedAsyncioTestCase):

    mock_play = AsyncMock()

    @patch(f"{TEST_MODULE}.LOGGER.error", new_callable=MagicMock)
    @patch(f"{TEST_MODULE}.SERVICE_HANDLERS", {"play_media": mock_play})
    async def asyncSetUp(self, mock_log: MagicMock):

        self.hass = MagicMock(spec=HomeAssistant)
        self.call = MagicMock(spec=ServiceCall)
        self.call.service = "play_media"
        self.error = ReadTimeoutError(MagicMock(), MagicMock(), MagicMock())
        self.mock_play.side_effect = self.error
        self.mock_log = mock_log
        self.handler = ServiceHandler(self.hass)

        await self.handler.async_relay_service_call(self.call)

    def test_error_log_called(self):
        try:
            self.mock_log.assert_called_with(self.error)
        except AssertionError:
            self.fail()
