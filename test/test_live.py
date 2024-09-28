"""Module for live testing"""

from unittest import TestCase, skipUnless

from custom_components.spotcast.spotify.account import (
    SpotifyAccount,
    SpotifyOAuth,
)

from custom_components.spotcast.media_player.chromecast_player import (
    Chromecast,
)

from custom_components.spotcast.chromecast.spotify_controller import (
    SpotifyController,
)

LIVE_TESTING = True


class TestLiveSetting(TestCase):

    def test_live_testing(self):
        oauth = SpotifyOAuth(
            client_id="423eb274904f441dbe5cc98bf8a05bd2",
            client_secret="d3e305f6ad144897865d88bdc9fc721d",
            redirect_uri="http://localhost:8123",
            scope=SpotifyAccount.SCOPE,
        )
        account = SpotifyAccount.from_spotipy_oauth(oauth)

        device = Chromecast.from_network(
            "192.168.0.131",
            friendly_name="Salon"
        )

        controller = SpotifyController(account)

        device.register_handler(controller)
        device.cast_info
        device.wait()
        device.start_app(controller.APP_ID)
        device.wait()
        controller.launch_app(device)
