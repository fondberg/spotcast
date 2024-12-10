import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.utils import get_account_entry, search_account
from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.websocket.utils import websocket_wrapper

ENDPOINT = "spotcast/tracks"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("playlistId"): cv.string,
        vol.Optional("account"): cv.string,
    }
)


@websocket_wrapper
async def async_tracks_handler(
    hass: HomeAssistant, connection: ActiveConnection, msg: dict
):
    """Gets the tracks of a playlist

    Args:
        - hass (HomeAssistant): The Home Assistant instance.
        - connection (ActiveConnection): The active WebSocket connection.
        - msg (dict): The message received through the WebSocket API.
    """
    account_id = msg.get("account")
    playlistId = msg.get("playlistId")

    account: SpotifyAccount

    if account_id is None:
        entry = get_account_entry(hass)
        account_id = entry.entry_id
        account = await SpotifyAccount.async_from_config_entry(hass, entry)
    else:
        account = search_account(hass, account_id)

    raw_tracks = await account.async_get_playlist_tracks(uri=playlistId)

    formatted_tracks = [
        {
            "id": track["track"]["id"],
            "name": track["track"]["name"],
            "href": track["track"]["href"],
            "album": track["track"].get("album", None),
            "artists": track["track"].get("artists", None),
        }
        for track in raw_tracks
    ]

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_tracks),
            "account": account_id,
            "tracks": formatted_tracks,
        },
    )
