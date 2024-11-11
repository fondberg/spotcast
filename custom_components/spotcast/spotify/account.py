"""Module for the spotify account class

Classes:
    - SpotifyAccount
"""

from logging import getLogger
from asyncio import (
    run_coroutine_threadsafe,
    sleep,
    TimeoutError,
)
from time import time
from typing import Any

from spotipy import Spotify, SpotifyException
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.sessions import (
    OAuth2Session,
    InternalSession,
    ConnectionSession,
    async_get_config_entry_implementation,
)
from custom_components.spotcast.spotify.dataset import Dataset

from custom_components.spotcast.spotify.exceptions import (
    PlaybackError,
)

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
        - image_link(str): the profile image image link
        - product(str): the current subscription product the user has
        - type(str): the type of account loaded
        - liked_songs_uri(str): the uri for the liked_songs playlist

    Constants:
        - SCOPE(tuple): A list of API permissions required for the
            instance to work properly
        - DJ_URI(str): the uri for the DJ playlist
        - REFRESH_RATE(int): rate at which to deem the cache deprecated

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
        - async_apply_extras
        - async_shuffle
        - async_liked_songs
        - async_repeat
        - async_set_volume

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

    DJ_URI = "spotify:playlist:37i9dQZF1EYkqdzj48dyYq"
    REFRESH_RATE = 30
    DATASETS = {
        "devices": {
            "refresh_rate": REFRESH_RATE,
            "can_expire": False,
        },
        "liked_songs": {
            "refresh_rate": REFRESH_RATE*2,
            "can_expire": False,
        },
        "playlists": {
            "refresh_rate": REFRESH_RATE*2,
            "can_expire": False,
        },
        "profile": {
            "refresh_rate": REFRESH_RATE*10,
            "can_expire": True,
        },
    }

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

        self._datasets = {x: Dataset(x, **y) for x, y in self.DATASETS.items()}

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
            name = self.id

        return name

    @property
    def profile(self) -> dict:
        """Returns the full profile dictionary of the account"""
        return self.get_dataset("profile")

    @property
    def playlists(self) -> list:
        """Returns the list of playlists for the account"""
        return self.get_dataset("playlists")

    @property
    def liked_songs(self) -> list:
        """Returns the list of liked songs for the account"""
        liked_songs = self.get_dataset("liked_songs")
        liked_songs = [x["track"]["uri"] for x in liked_songs]
        return liked_songs

    @property
    def devices(self) -> list:
        """Returns the list of devices linked to the account"""
        return self.get_dataset("devices")

    @property
    def country(self) -> str:
        """Returns the current country in which the account resides"""
        return self.get_profile_value("country")

    @property
    def image_link(self) -> str:
        """Returns the link for the account profile image"""
        images = self.get_profile_value("images")
        image_url = None
        max_area = 0

        for image in images:

            area = image["width"] * image["height"]

            if area > max_area:
                image_url = image["url"]
                max_area = area

        return image_url

    @property
    def product(self) -> str:
        """Returns the account subscription product"""
        return self.get_profile_value("product")

    @property
    def type(self) -> str:
        """Returns the type of account"""
        return self.get_profile_value("type")

    @property
    def liked_songs_uri(self) -> str:
        """Returns the liked songs uri for the account"""
        return f"spotify:user:{self.id}:collection"

    @property
    def device_info(self) -> DeviceInfo:
        """Returns the Home Assistant device info of the Account
        Service"""
        return DeviceInfo(
            identifiers={(DOMAIN, self.id)},
            manufacturer="Spotify AB",
            model=f"Spotify {self.profile['product']}",
            name=f"Spotcast {self.name}",
            entry_type=DeviceEntryType.SERVICE,
            configuration_url="https://open.spotify.com",
        )

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
        profile = self._datasets["profile"].data

        return profile.get(attribute)

    def get_dataset(self, name: str) -> list | dict:
        return self._datasets[name].data

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

    async def async_ensure_tokens_valid(self, skip_profile: bool = False):
        """Ensures the token are valid

        Args:
            - skip_profile(bool, optional): set True to skip the
                profile update. Defaults to False
        """

        if not skip_profile:
            await self.async_profile()

        LOGGER.debug(
            "Refreshing api tokens for Spotify Account"
        )
        for key, session in self.sessions.items():
            await session.async_ensure_token_valid()

            if key == "external":
                token = await self.async_get_token(key)
                self._spotify.set_auth(token["access_token"])

    async def async_profile(self, force: bool = False) -> dict:
        """Test the connection and returns a user profile

        Args:
            - force(bool, optional): Forces the profile update if True.
                Defaults to False

        Returns:
            - dict: the raw profile dictionary from the Spotify API
        """
        await self.async_ensure_tokens_valid(skip_profile=True)
        LOGGER.debug("Getting Profile from Spotify")

        dataset = self._datasets["profile"]

        if force or dataset.is_expired:
            LOGGER.debug("Refreshing profile dataset")
            async with dataset.lock:
                data = await self.hass.async_add_executor_job(self._spotify.me)
                dataset.update(data)
        else:
            LOGGER.debug("Using cached profile dataset")

        return self.profile

    async def async_devices(self, force: bool = False) -> list[dict]:
        """Returns the list of devices"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Devices for account `%s`", self.name)

        dataset = self._datasets["devices"]

        if force or dataset.is_expired:
            LOGGER.debug("Refreshing devices dataset")
            async with dataset.lock:
                data = await self.hass.async_add_executor_job(
                    self._spotify.devices
                )
                dataset.update(data["devices"])
        else:
            LOGGER.debug("Using Cached devices dataset")

        return self.devices

    async def async_playlists(self, force: bool = False) -> list[dict]:
        """Returns a list of playlist for the current user"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Playlist for account `%s`", self.name)

        dataset = self._datasets["playlists"]

        if force or dataset.is_expired:
            LOGGER.debug("Refreshing playlists dataset")
            async with dataset.lock:

                offset = 0
                all_playlists = []
                total = None

                while total is None or len(all_playlists) < total:

                    current_playlists: dict = await self.hass\
                        .async_add_executor_job(
                            self._spotify.current_user_playlists,
                            50,
                            offset,
                        )

                    if total is None:
                        total = current_playlists["total"]

                    all_playlists.extend(current_playlists["items"])
                    offset = len(all_playlists)

                dataset.update(all_playlists)
        else:
            LOGGER.debug("Using cached playlists dataset")

        return self.playlists

    async def async_wait_for_device(self, device_id: str, timeout: int = 12):
        """Asycnhronously wait for a device to become available

        Args:
            - device_id(str): the spotify id of the device to wait for
            - timeout(int): the timeout delay to wait for before
                raising an error.

        Raises:
            - TimeoutError: raised when waiting for the device goes
                beyond the set delay
        """
        LOGGER.debug("Waiting for device `%s` to become available", device_id)

        end_time = time() + timeout

        while (time() <= end_time):

            devices = await self.async_devices(force=True)
            devices = {x["id"]: x for x in devices}

            try:
                devices[device_id]
                return
            except KeyError:
                LOGGER.debug("Device `%s` not yet available", device_id)
                await sleep(timeout/4)

        raise TimeoutError(
            f"device `{device_id}` still not available after {timeout} sec."
        )

    async def async_apply_extras(
            self,
            device_id: str,
            extras: dict,
    ):
        """Applies extra settings on an account

        Args:
            - account(SpotifyAccount): the account to apply extras to
            - device_id(str): the device to set the extras to
            - extras(dict): the extra settings to apply
        """
        actions = {
            "start_volume": self.async_set_volume,
            "shuffle": self.async_shuffle,
            "repeat": self.async_repeat,
        }

        for key, value in extras.items():

            if key not in actions:
                continue

            await actions[key](value, device_id)

    async def async_play_media(
        self,
        device_id: str,
        context_uri: str = None,
        uris: list[str] = None,
        offset: int = None,
        position_ms: int = None,
        **_
    ):
        """Play the media linked to the uri provided on the device id
        requested

        Args:
            - device_id(str): The spotify device id to play media on
            - context_uri(str): The uri of the media to play

        Raises:
            - PlaybackError: raised when spotipy raises an error while
                trying to start playback
        """
        await self.async_ensure_tokens_valid()

        LOGGER.info(
            "Starting playback of `%s` on device `%s`",
            context_uri,
            device_id
        )

        try:
            await self.hass.async_add_executor_job(
                self._spotify.start_playback,
                device_id,
                context_uri,
                uris,
                offset,
                position_ms,
            )
        except SpotifyException as exc:
            raise PlaybackError(exc.msg) from exc

    async def async_shuffle(
        self,
        shuffle: bool,
        device_id: str,
    ):
        """Sets the shuffle mode for a device

        Args:
            - shuffle(bool): Sets the shuffle mode to True or False
                based on the value provided
            - device_id(str): the device to set the shuffle mode on
        """
        await self.async_ensure_tokens_valid()

        LOGGER.info(
            "Setting shuffle to %s on device `%s`",
            str(shuffle),
            device_id
        )

        await self.hass.async_add_executor_job(
            self._spotify.shuffle,
            shuffle,
            device_id,
        )

    async def async_liked_songs(self, force: bool = False) -> list[str]:
        """Retrieves the list of uris of songs in the user liked songs
        """
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting saved tracks for account `%s`", self.name)

        dataset = self._datasets["liked_songs"]

        if force or dataset.is_expired:
            LOGGER.debug("Refreshing liked songs dataset")
            async with dataset.lock:

                offset = 0
                liked_songs = []
                total = None

                while total is None or len(liked_songs) < total:

                    current_songs: dict = await self.hass\
                        .async_add_executor_job(
                            self._spotify.current_user_saved_tracks,
                            50,
                            offset,
                        )

                    if total is None:
                        total = current_songs["total"]

                    liked_songs.extend(current_songs["items"])
                    offset = len(liked_songs)

                dataset.update(liked_songs)
        else:
            LOGGER.debug("Using cached liked songs dataset")

        return self.liked_songs

    async def async_repeat(
        self,
        state: str,
        device_id: str,
    ):
        """Sets the repeat mode for a device

        Args:
            - state(str): Sets the repeat mode for the device
            - device_id(str): the device to set the repeat mode
        """
        await self.async_ensure_tokens_valid()

        LOGGER.info(
            "Setting repeat state to %s on device `%s`",
            str(state),
            device_id
        )

        await self.hass.async_add_executor_job(
            self._spotify.repeat,
            state,
            device_id,
        )

    async def async_set_volume(
        self,
        volume: int,
        device_id: str,
    ):
        """Sets the volume level for a device

        Args:
            - volume(int): The percentage of volume to set
            - device_id(str): the device to set the repeat mode
        """
        await self.async_ensure_tokens_valid()

        LOGGER.info(
            "Setting volume to %d%% for device `%s`",
            volume,
            device_id
        )

        await self.hass.async_add_executor_job(
            self._spotify.volume,
            volume,
            device_id,
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
        if DOMAIN not in hass.data:
            hass.data[DOMAIN] = {}

        account = hass.data[DOMAIN].get(entry.entry_id)

        if account is not None:
            LOGGER.debug(
                "Providing preexisting account for entry `%s`",
                entry.entry_id
            )
            return account

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

        LOGGER.debug(
            "Adding entry `%s` to spotcast data entries",
            entry.entry_id,
        )
        hass.data[DOMAIN][entry.entry_id] = account

        return account
