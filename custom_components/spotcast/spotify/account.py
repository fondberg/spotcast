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
from homeassistant.config_entries import ConfigEntry, SOURCE_REAUTH
from homeassistant.helpers.device_registry import DeviceInfo, DeviceEntryType

from custom_components.spotcast.const import DOMAIN
from custom_components.spotcast.sessions import (
    PublicSession,
    PrivateSession,
    ConnectionSession,
    async_get_config_entry_implementation,
)
from custom_components.spotcast.utils import ensure_default_data
from custom_components.spotcast.spotify.dataset import Dataset
from custom_components.spotcast.spotify.search_query import SearchQuery
from custom_components.spotcast.spotify.utils import select_image_url
from custom_components.spotcast.spotify.exceptions import (
    PlaybackError,
    TokenError,
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
        - REFRESH_RATE(int): default rate at which to deem the cache
            deprecated
       - DATASETS(dict[str, dict]): Default configuration for datasets
            used by the account

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
            "refresh_factor": 1,
            "can_expire": False,
        },
        "liked_songs": {
            "refresh_factor": 10,
            "can_expire": False,
        },
        "playlists": {
            "refresh_factor": 10,
            "can_expire": False,
        },
        "profile": {
            "refresh_factor": 20,
            "can_expire": True,
        },
        "categories": {
            "refresh_factor": 20,
            "can_expire": False,
        },
        "playback_state": {
            "refresh_factor": 1/2,
            "can_expire": False,
        },
    }

    def __init__(
            self,
            entry_id: str,
            hass: HomeAssistant,
            public_session: PublicSession,
            private_session: PrivateSession,
            is_default: bool = False,
            base_refresh_rate: int = 30
    ):
        """The account of a Spotify user. Able to leverage the public
        and private API.

        Args:
            - entry_id(str): The id of the config entry in HomeAssistant
                for the account.
            - hass(HomeAssistant): The Home Assistant Instance
            - external_session(OAuth2Session): The public api session
                for the Spotify Account
            - internal_session(InternalSession): The private api
                session for the Spotify Account
            - is_default(bool, optional): True if account is treated as
                default for service call. Defaults to False.
            - base_refresh_rate(int, optional): The base refresh rate
                used to update dateset
        """
        self.entry_id = entry_id
        self.hass = hass
        self.sessions: dict[str, ConnectionSession] = {
            "public": public_session,
            "private": private_session,
        }
        self.apis: dict[str, Spotify] = {}

        for name, session in self.sessions.items():
            self.apis[name] = Spotify(auth=session.token)

        self.is_default = is_default
        self._base_refresh_rate = 30

        self._datasets: dict[str, Dataset] = {}
        self.last_playback_state = {}
        self.current_item = {
            "uri": None,
            "audio_features": {}
        }

        for name, dataset in self.DATASETS.items():
            refresh_rate = dataset["refresh_factor"] * self._base_refresh_rate
            can_expire = dataset["can_expire"]
            self._datasets[name] = Dataset(name, refresh_rate, can_expire)

    @property
    def base_refresh_rate(self) -> int:
        """Returns the current base refresh rate """
        return self._base_refresh_rate

    @base_refresh_rate.setter
    def base_refresh_rate(self, value: int):
        """Sets the base refresh rate and updates the dataset
        accordingly

        Args:
            - value(int): the new base refresh_rate
        """
        self._base_refresh_rate = value

        for name, dataset in self._datasets.items():
            refresh_factor = self.DATASETS[name]["refresh_factor"]
            dataset.refresh_rate = value * refresh_factor

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
    def categories(self) -> list:
        """Returns the list of Browse categories for the account"""
        return self.get_dataset("categories")

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
    def playback_state(self) -> list:
        """Returns the list of devices linked to the account"""
        return self.get_dataset("playback_state")

    @property
    def country(self) -> str:
        """Returns the current country in which the account resides"""
        return self.get_profile_value("country")

    @property
    def image_link(self) -> str:
        """Returns the link for the account profile image"""
        images = self.get_profile_value("images")
        return select_image_url(images)

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

    @property
    def health_status(self) -> dict[str, bool]:
        """Returns the health status of the underlying sessions"""

        health = {}

        for key, session in self.sessions.items():
            health[key] = session.is_healthy

        return health

    @property
    def active_device(self) -> str:
        """returns the current active device, or None if no active
        device"""

        playback_state = self.playback_state

        if self.playback_state == {}:
            return None

        return playback_state["device"]["id"]

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
        return self.sessions[api].clean_token

    async def async_ensure_tokens_valid(
            self,
            skip_profile: bool = False,
            reauth_on_fail: bool = True,
    ):
        """Ensures the token are valid

        Args:
            - skip_profile(bool, optional): set True to skip the
                profile update. Defaults to False
            - reauth_on_fail(bool, optional): Asks for reauthorisation
                of the entry on failure to get token. Defaults to True.
        """

        if not skip_profile:
            await self.async_profile()

        LOGGER.debug(
            "Refreshing api tokens for Spotify Account"
        )
        for key, session in self.sessions.items():

            try:
                await session.async_ensure_token_valid()
            except TokenError as exc:

                if reauth_on_fail:

                    entry = self.hass.config_entries.async_get_entry(
                        self.entry_id
                    )

                    entry.async_start_reauth(
                        self.hass,
                        context={"source": SOURCE_REAUTH}
                    )

                raise exc

            token = await self.async_get_token(key)
            self.apis[key].set_auth(token)

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

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing profile dataset")
                data = await self.hass.async_add_executor_job(
                    self.apis["private"].me
                )
                dataset.update(data)
            else:
                LOGGER.debug("Using cached profile dataset")

        return self.profile

    async def async_devices(self, force: bool = False) -> list[dict]:
        """Returns the list of devices"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Devices for account `%s`", self.name)

        dataset = self._datasets["devices"]

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing devices dataset")
                data = await self.hass.async_add_executor_job(
                    self.apis["public"].devices
                )
                dataset.update(data["devices"])
            else:
                LOGGER.debug("Using Cached devices dataset")

        return self.devices

    async def async_saved_episodes(
            self,
            limit: int = None,
    ) -> list[dict]:
        """Retrieves the list of podcast episode saved to the user
        account

        Args:
            - limit(int, optional): If not None, stops getting episode
                once the limit of item reached. Defaults to None

        Return:
            - list[dict]: a list of dictionary with the episodes
                information
        """

        await self.async_ensure_tokens_valid()
        LOGGER.debug(
            "Getting List of saved podcast episode for account `%s`",
            self.name,
        )

        return await self._async_pager(
            self.apis["private"].current_user_saved_episodes,
            appends=[self.country],
            max_items=limit,
        )

    async def async_get_track(self, uri: str) -> dict:
        """Retrieves track information

        Args:
            - uri(str): The URI of the track to search

        Returns:
            - dict: the songs details
        """
        await self.async_ensure_tokens_valid()

        LOGGER.debug("Getting track information for `%s`", uri)

        result = await self.hass.async_add_executor_job(
            self.apis["private"].track,
            uri,
            self.country
        )

        return result

    async def async_get_playlist(self, uri: str) -> dict:
        """Retrieves a playlist information

        Args:
            - uri(str): the URI of the playlist to search

        Returns:
            - dict: the playlist details
        """

        playlist_id = uri.rsplit(":", maxsplit=1)[-1]

        result = await self.hass.async_add_executor_job(
            self.apis["private"].playlist,
            playlist_id,
            None,
            self.country,
        )

        return result

    async def async_get_album(self, uri: str) -> dict:
        """Retrieves an album information

        Args:
            - uri(str): the URI of the album to search

        Returns:
            - dict: the album details
        """

        album_id = uri.rsplit(":", maxsplit=1)[-1]

        result = await self.hass.async_add_executor_job(
            self.apis["private"].album,
            album_id,
            self.country,
        )

        return result

    async def async_get_artist_top_tracks(self, uri: str) -> list[dict]:
        """Retrieves the list of top tracks for an artist

        Args:
            - uri(str): the URI of the artist to search

        Returns:
            - list[dict]: the list of top songes for an artist
        """

        result = await self.hass.async_add_executor_job(
            self.apis["private"].artist_top_tracks,
            uri,
            self.country,
        )

        return result["tracks"]

    async def async_playback_state(self, force: bool = False) -> dict:
        """Returns the current playback state"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Playback Sate for account `%s`", self.name)

        dataset = self._datasets["playback_state"]

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing playback state dataset")
                data = await self.hass.async_add_executor_job(
                    self.apis["private"].current_playback,
                    self.country,
                )

                data = {} if data is None else data

                if data != {}:
                    data = await self._async_add_audio_features(data)

                dataset.update(data)
            else:
                LOGGER.debug("Using Cached playback state dataset")

        return self.playback_state

    async def _async_add_audio_features(self, playback_state: dict) -> dict:
        """Adds the audio_features to the current playback state"""
        current_uri = playback_state["item"]["uri"]
        last_uri = self.current_item["uri"]

        if current_uri != last_uri:
            audio_features = await self.async_track_features(current_uri)
            self.current_item["audio_features"] = audio_features

        playback_state["audio_features"] = self.current_item["audio_features"]
        return playback_state

    async def async_track_features(self, uri: str) -> str:
        """Returns the track audio features. Returns an empty
        dictionary if the item doesn't have audio features"""
        if uri is None or not uri.startswith("spotify:track:"):
            return {}

        return await self.hass.async_add_executor_job(
            self.apis["private"].audio_features(uri)
        )

    async def async_playlists_count(self) -> int:
        """Returns the number of user playlist for an account"""

        return await self._async_get_count(
            self.apis["private"].current_user_playlists
        )

    async def async_playlists(
            self,
            force: bool = False,
            max_items: int = None
    ) -> list[dict]:
        """Returns a list of playlist for the current user"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Playlist for account `%s`", self.name)

        dataset = self._datasets["playlists"]

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing playlists dataset")

                playlists = await self._async_pager(
                    self.apis["private"].current_user_playlists,
                    max_items=max_items,
                )

                dataset.update(playlists)

            else:
                LOGGER.debug("Using cached playlists dataset")

        return self.playlists

    async def async_search(
            self,
            query: SearchQuery,
            max_items: int = 20
    ) -> list[dict]:
        """Makes a search query and returns the result"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug(
            "Getting Search Result `%s` for account `%s`",
            query.search,
            self.name,
        )

        limit = 50

        if max_items < limit:
            limit = max_items

        search_result = await self._async_pager(
            function=self.apis["private"].search,
            prepends=[query.query_string],
            appends=[query.item_type, self.country],
            limit=limit,
            sub_layer=f"{query.item_type}s",
            max_items=max_items,
        )

        return search_result

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
            "volume": self.async_set_volume,
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
        position: int = None,
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

        if offset is not None:
            offset = {"position": offset}

        if position is not None:
            position = int(position * 1000)

        try:
            await self.hass.async_add_executor_job(
                self.apis["private"].start_playback,
                device_id,
                context_uri,
                uris,
                offset,
                position,
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
            self.apis["private"].shuffle,
            shuffle,
            device_id,
        )

    async def async_liked_songs_count(self) -> int:
        """returns the number of linked songs for an account"""
        return await self._async_get_count(
            self.apis["private"].current_user_saved_tracks,
        )

    async def async_liked_songs(self, force: bool = False) -> list[str]:
        """Retrieves the list of uris of songs in the user liked songs
        """
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting saved tracks for account `%s`", self.name)

        dataset = self._datasets["liked_songs"]

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing liked songs dataset")

                liked_songs = await self._async_pager(
                    self.apis["private"].current_user_saved_tracks,
                )

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
            self.apis["private"].repeat,
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
            self.apis["private"].volume,
            volume,
            device_id,
        )

    async def async_categories(
            self,
            force: bool = False,
            limit: int = None,
    ) -> list[dict]:
        """Fetches the categories available for the account"""
        await self.async_ensure_tokens_valid()
        LOGGER.debug("Getting Browse Categories for account `%s`", self.name)

        dataset = self._datasets["categories"]

        async with dataset.lock:
            if force or dataset.is_expired:
                LOGGER.debug("Refreshing Browse Categories dataset")

                categories = await self._async_pager(
                    self.apis["private"].categories,
                    prepends=[self.country, None],
                    sub_layer="categories",
                    max_items=limit,
                )

                dataset.update(categories)
            else:
                LOGGER.debug("Using cached Browse Categories dataset")

        return self.categories

    async def async_category_playlists(
            self,
            category_id: str,
            limit: int = None,
    ) -> list[str]:
        """Fetches the playlist associated with a browse category

        Args:
            - category_id(str): the id of of the category to retreive
                playlists from
            - limit(int, optional): the maxmimum number of item to
                retrieve. Retrieves all if None. Defaults to None.

        Returns:
            - list[str]: list of playlists linked to the category id
                provided
        """
        await self.async_ensure_tokens_valid()
        LOGGER.debug(
            "Retrieving playlist linked to category id `%s`",
            category_id,
        )

        playlists = await self._async_pager(
            self.apis["private"].category_playlists,
            prepends=[category_id, self.country],
            sub_layer="playlists",
            max_items=limit,
        )

        return playlists

    async def _async_get_count(
            self,
            function: callable,
            prepends: list = None,
            appends: list = None,
            sub_layer: str = None,
            max_items: int = None,
    ) -> int:
        """Returns the number of item in a specific pagination

        Args:
            - function(callable): the function to call to retrieve
                content. Must be able to take a `limit` and `offset`
                arguments.
            - preppends: arguments to pass to the function on
                each call before the limit and offset
            - appends: arguments to pass to the function on
                each call after the limit and offset
            - sub_layer(str, optional): sub key in the response
                containing the pagination. Use the response as a
                pagination if None. Defaults to None.

        Returns:
            - int: the number of items in the pagination
        """
        prepends = [] if prepends is None else prepends
        appends = [] if appends is None else appends
        arguments = [*prepends, 1, 0, *appends]

        result = await self.hass.async_add_executor_job(
            function,
            *arguments,
        )

        if sub_layer is not None:
            result = result[sub_layer]

        return result["total"]

    async def _async_pager(
            self,
            function: callable,
            prepends: list = None,
            appends: list = None,
            limit: int = 50,
            sub_layer: str = None,
            max_items: int = None,
    ) -> list[dict]:
        """Retrieves data from an api endpoint using a paging
        generator logic

        Args:
            - function(callable): the function to call to retrieve
                content. Must be able to take a `limit` and `offset`
                arguments.
            - preppends: arguments to pass to the function on
                each call before the limit and offset
            - appends: arguments to pass to the function on
                each call after the limit and offset
            - limit(int, optional): the maximum number of items to
                retrieve in a single call, defaults to 50
            - sub_layer(str, optional): sub key in the response
                containing the pagination. Use the response as a
                pagination if None. Defaults to None.
            - max_items(int, optional): the maximum number of items to
                retrieve. Retrieve all items if None. Defaults to None.

        Returns:
            - Generator[list[dict], None, None]
        """
        offset = 0
        items = []
        total = max_items
        prepends = [] if prepends is None else prepends
        appends = [] if appends is None else appends

        while total is None or len(items) < total:

            arguments = [*prepends, limit, offset, *appends]

            result = await self.hass.async_add_executor_job(
                function,
                *arguments
            )

            if sub_layer is not None:
                result = result[sub_layer]

            if total is None:
                total = result["total"]

            current_items = result["items"]

            if (delta := total - (len(items) + len(result["items"]))) < 0:
                current_items = current_items[:delta]

            items.extend(current_items)
            offset = len(items)

        items = [x for x in items if x is not None]

        return items

    async def async_add_to_queue(self,  uri: str, device_id: str = None):
        """Adds an item to the playback queue

        Args:
            - uri(str): the spotify item to add to the queue
            - device_id(str, optional): The id of the device this
                command is targeting. If None, the account's currently
                active device is the target. Defaults to None.
        """
        await self.async_ensure_tokens_valid()

        try:
            await self.hass.async_add_executor_job(
                self.apis["private"].add_to_queue,
                uri,
                device_id,
            )
        except SpotifyException as exc:
            raise PlaybackError(
                f"Could not add `{uri}` to device `{device_id}`"
            ) from exc

    @staticmethod
    async def async_from_config_entry(
            hass: HomeAssistant,
            entry: ConfigEntry,
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

        hass = ensure_default_data(hass, entry.entry_id)
        domain_data = hass.data[DOMAIN]

        account = domain_data[entry.entry_id].get("account")

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

        public_session = PublicSession(hass, entry, oauth_implementation)
        await public_session.async_ensure_token_valid()

        private_session = PrivateSession(hass, entry)
        await private_session.async_ensure_token_valid()

        account = SpotifyAccount(
            entry_id=entry.entry_id,
            hass=hass,
            public_session=public_session,
            private_session=private_session,
            **entry.options
        )

        await account.async_profile()

        LOGGER.debug(
            "Adding entry `%s` to spotcast data entries",
            entry.entry_id,
        )
        hass.data[DOMAIN][entry.entry_id]["account"] = account

        return account
