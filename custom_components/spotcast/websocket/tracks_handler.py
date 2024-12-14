import voluptuous as vol
from homeassistant.helpers import config_validation as cv
from homeassistant.core import HomeAssistant
from homeassistant.components.websocket_api import ActiveConnection

from custom_components.spotcast.websocket.utils import (
    websocket_wrapper,
    async_get_account,
)

ENDPOINT = "spotcast/tracks"
SCHEMA = vol.Schema(
    {
        vol.Required("id"): cv.positive_int,
        vol.Required("type"): ENDPOINT,
        vol.Required("playlist_id"): cv.string,
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
    playlist_id = msg.get("playlist_id")

    account = await async_get_account(hass, account_id)

    tracks = await account.async_get_playlist_tracks(uri=playlist_id)

    formatted_tracks = []

    for track in tracks:

        track = track["track"]

        formatted_tracks.append({
            "id": track.get("id"),
            "name": track.get("name"),
            "uri": track.get("uri"),
            "album": track.get("album"),
            "artists": track.get("artists")
        })

    connection.send_result(
        msg["id"],
        {
            "total": len(formatted_tracks),
            "account": account.id,
            "tracks": formatted_tracks,
        },
    )
