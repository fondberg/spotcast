"""Module to test the async_update function"""

from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, patch, MagicMock


from custom_components.spotcast.sessions.exceptions import InternalServerError
from custom_components.spotcast.sensor.abstract_entity import (
    SpotcastEntity,
    EntityCategory,
    SpotifyAccount,
    STATE_UNKNOWN,
)


class DummyEntity(SpotcastEntity):

    PLATFORM = "dummy"
    ENTITY_CATEGORY = EntityCategory.CONFIG

    @property
    def _default_attributes(self):
        return {"foo": []}

    @property
    def icon(self):
        """Unimplemented icon property"""

    async def _async_update_process():
        """Unimplemented async_update_process"""


class TestWorkingUpdate(IsolatedAsyncioTestCase):

    @patch.object(DummyEntity, "_async_update_process")
    async def asyncSetUp(self, mock_update: AsyncMock):

        self.mocks = {
            "update": mock_update,
            "account": MagicMock(spec=SpotifyAccount)
        }

        self.entity = DummyEntity(self.mocks["account"])
        self.entity._attr_state = "FOO"
        await self.entity.async_update()

    def test_state_unachanged(self):
        self.assertEqual(self.entity._attr_state, "FOO")


class TestFailedUpdate(IsolatedAsyncioTestCase):

    @patch.object(DummyEntity, "_async_update_process")
    async def asyncSetUp(self, mock_update: AsyncMock):

        self.mocks = {
            "update": mock_update,
            "account": MagicMock(spec=SpotifyAccount),
        }

        self.mocks["update"].side_effect = InternalServerError(
            429,
            "Dummy Error"
        )

        self.entity = DummyEntity(self.mocks["account"])
        self.entity._attr_state = "FOO"
        self.entity._attributes = {"foo": [1, 2, 3]}
        await self.entity.async_update()

    def test_state_changed_to_unknown(self):
        self.assertEqual(self.entity._attr_state, STATE_UNKNOWN)

    def test_attributes_resetted(self):
        self.assertEqual(self.entity._attributes, {"foo": []})
