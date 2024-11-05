"""Module for the spotify account class

Classes:
    - SpotifyAccount
"""

from logging import getLogger
from asyncio import run_coroutine_threadsafe
from asyncio import sleep
from time import time
from typing import Any

from spotipy import Spotify
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
    ConnectionSession,
    async_get_config_entry_implementation,
)

from custom_components.spotcast.spotify.exceptions import ProfileNotLoadedError

LOGGER = getLogger(__name__)


class SpotifyAccount:
    """The account of a Spotify user. Able to leverage the public and
    private API.

    Attributes:
        - hass(HomeAssistant): The Home Assistance instance
        - sessions(dict[str, ConnectionSession]): A dictionary with
            both the Internal (Private) and External (Public) API
            access
        - is_defaults(bool): set to True if the account should be
            treated as default when calling services

    Properties:
        - id(str): the identifier of the account
        - name(str): the dusplay name for the account
        - profile(dict): the full profile dictionary of the account
        - country(str): the country code where the account currently
            is.

    Constants:
        - SCOPE(tuple): A list of API permissions required for the
            instance to work properly

    Methods:
        - get_profile_value
        - get_token
        - async_get_token
        - async_connect
        - async_ensure_tokens_valid
        - async_profile
        - async_devices
        - async_playlists
        - async_wait_for_devices
        - async_register_chromecast_player
        - async_play_media

    Functions:
        - async_from_config_entry
    """

    SCOPE = (
        "user-modify-playback-state",
        "user-read-playback-state",
        "user-read-private",
        "playlist-read-private",
        "playlist-read-collaborative",
        "user-library-read",
        "user-top-read",
        "user-read-playback-position",
        "user-read-recently-played",
        "user-follow-read",
    )

    def __init__(
            self,
            hass: HomeAssistant,
            external_session: OAuth2Session,
            internal_session: InternalSession,
            is_default: bool = False,
    ):
        """The account of a Spotify user. Able to leverage the public
        and private API.

        Args:
            - hass(HomeAssistant): The Home Assistant Instance
            - external_session(OAuth2Session): The public api session
                for the Spotify Account
            - internal_session(InternalSession): The private api
                session for the Spotify Account
            - is_default(bool, optional): True if account is treated as
                default for service call. Defaults to False.
        """
        self.hass = hass
        self.sessions: dict[str, ConnectionSession] = {
            "external": external_session,
            "internal": internal_session,
        }
        self.is_default = is_default

        self._spotify = Spotify(
            auth=self.sessions["external"].token["access_token"]
        )

        self._profile = {}

    @property
    def id(self) -> str:
        """Returns the id of the account"""
        return self.get_profile_value("id")

    @property
    def name(self) -> str:
        """Returns the name of the account. In case of no display name,
        returns the id
        """
        name = self.get_profile_value("display_name")

        if name is None:
            name = self.get_profile_value("id")

        return name

    @property
    def profile(self) -> dict:
        """Returns the full profile dictionary of the account"""
        self.get_profile_value("id")
        return self._profile

    @property
    def country(self) -> str:
        """Returns the current country in which the account resides"""
        return self.get_profile_value("country")

    def get_profile_value(self, attribute: str) -> Any:
        """Returns the value for a profile element. Raises Error if not
        yet loaded.

        Args:
            - attribute(str): the attribute to fetch from the profile

        Raises:
            - ProfileNotLoadedError: Raised if the profile hasn't been
                loaded yet.

        Returns:
            - Any: the value at the key in the profile
        """
        if self._profile == {}:
            raise ProfileNotLoadedError(
                "The profile has not been loaded properly in the account. Call"
                " `async_profile`"
            )

        return self._profile.get(attribute)

    def get_token(self, api: str) -> str:
        """Retrives a token from the requested session.

        Args:
            - api(str): The api to retrieve from. Cann be `internal`
                or `external`.

        Returns:
            - str: token for the requested session
        """
        return run_coroutine_threadsafe(
            self.async_get_token(api),
            self.hass.loop
        ).result()

    async def async_get_token(self, api: str) -> str:
        """Retrives a token from the requested session.

        Args:
            - api(str): The api to retrieve from. Can be `internal` or
                `external`.

        Returns:
            - str: token for the requested session
        """
        await self.sessions[api].async_ensure_token_valid()
        return self.sessions[api].token

    async def async_connect(self) -> "SpotifyAccount":
        """Ensure conncetion and return itself"""
        await self.async_ensure_tokens_valid()
        token = await self.async_get_token("external")
        self._spotify.set_auth(token)
        return self

    async def async_ensure_tokens_valid(self):
        """Ensures the token are valid"""
        LOGGER.debug("Refreshing api tokens for Spotify Account")
        for key, session in self.sessions.items():
            await session.async_ensure_token_valid()

    async def async_profile(self) -> dict:
        """Test the connection and returns a user profile"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Profile from Spotify")
        self._profile: dict = await self.hass.async_add_executor_job(
            self._spotify.me
        )

        self.name

        return self.profile

    async def async_devices(self) -> list[dict]:
        """Returns the list of devices"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Devices for account `%s`", self.name)
        response = await self.hass.async_add_executor_job(
            self._spotify.devices
        )

        devices = response["devices"]

        # Log all the devices found
        for device in devices:
            LOGGER.debug("Found Device [%s](%s)", device["name"], device["id"])

        return devices

    async def async_playlists(self) -> list[dict]:
        """Returns a list of playlist for the current user"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Playlist for account `%s`", self.name)

        offset = 0
        all_playllists = []
        total = None

        while total is None or len(all_playllists) < total:

            current_playlist: dict = await self.hass.async_add_executor_job(
                self._spotify.current_user_playlists,
                50,
                offset
            )

            if total is None:
                total = current_playlist["total"]

            all_playllists.extend(current_playlist["items"])
            offset = len(all_playllists)

        return all_playllists

    async def async_wait_for_device(self, device_id: str, timeout: int = 12):
        """Asycnhronously wait for a device to become available"""
        LOGGER.debug("Waiting for device `%s` to become available", device_id)

        end_time = time() + timeout

        while (time() <= end_time):

            devices = await self.async_devices()
            devices = {x["id"]: x for x in devices}

            try:
                devices[device_id]
                return
            except KeyError:
                LOGGER.debug("Device `%s` not yet available", device_id)
                await sleep(1)

        raise TimeoutError(
            f"device `{device_id}` still not available after {timeout} sec."
        )

    async def async_play_media(self, device_id: str, context_uri: str):
        """Play the media linked to the uri provided on the device id
        requested

        Args:
            - device_id(str): The spotify device id to play media on
            - context_uri(str): The uri of the media to play
        """

        await self.async_ensure_tokens_valid()

        LOGGER.info(
            "Starting playback of `%s` on device `%s`",
            context_uri,
            device_id
        )

        await self.hass.async_add_executor_job(
            self._spotify.start_playback,
            device_id,
            context_uri,
        )

    @staticmethod
    async def async_from_config_entry(
            hass: HomeAssistant,
            entry: ConfigEntry
    ) -> "SpotifyAccount":
        """Builds a Spotify Account from the home assistant config
        entry

        Args:
            - hass(HomeAssistant): the HomeAssistant Instance object
            - entry(ConfigEntry): the config entry for the spotify
                account being setup
        Returns:
            SpotifyAccount: A spotify account from the api config in
                the config entry
        """
        oauth_implementation = await async_get_config_entry_implementation(
            hass=hass,
            config_entry=entry,
        )

        external_api = OAuth2Session(hass, entry, oauth_implementation)
        await external_api.async_ensure_token_valid()

        internal_api = InternalSession(hass, entry)
        await internal_api.async_ensure_token_valid()

        is_default = "is_default" in entry.data and entry.data["is_default"]

        account = SpotifyAccount(hass, external_api, internal_api, is_default)
        await account.async_profile()

        return account
