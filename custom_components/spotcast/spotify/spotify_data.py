"""Module for the SpotifyData class"""

from typing import Any

from custom_components.spotcast.spotify.account import SpotifyAccount
from custom_components.spotcast.spotify.dataset import Dataset


class SpotifyData:
    """A collection of dataset for a spotify account"""

    DATASETS = {
        "devices": {
            "refresh_factor": 1,
            "can_expire": False,
        },
        "liked_songs": {
            "refresh_factor": 4,
            "can_expire": False,
        },
        "playlists": {
            "refresh_factor": 2,
            "can_expire": False,
        },
        "profile": {
            "refresh_factor": 10,
            "can_expire": True,
        },
        "categories": {
            "refresh_factor": 10,
            "can_expire": False,
        },
        "playback_state": {
            "refresh_factor": 1/2,
            "can_expire": False,
        }
    }

    def __init__(self, account: SpotifyAccount):

        self._account = account
        self._datasets: dict[str, Dataset] = {}

        functions = {
            "devices": account.apis["public"].get_devices,
            "liked_songs": account.apis["private"].get_saved_tracks,
            "playlists": account.apis[
                "private"
            ].get_playlists_for_current_user,
            "profile": account.apis["private"].get_current_user,
            "categories": account.apis["private"].get_categories,
            "playback_state": account.apis["private"].get_playback,
        }

        for name, arguments in self.DATASETS.items():
            function = functions.get(name)
            refresh_rate = self._account.base_refresh_rate
            refresh_rate *= arguments["refresh_factor"]
            can_expire = arguments["can_expire"]
            self._datasets[name] = Dataset(
                name=name,
                refresh_function=function,
                refresh_rate=refresh_rate,
                can_expire=can_expire
            )

    def update_refresh_rate(self):
        """Updates all datasets refresh rate according to the current
        base refresh rate of the account"""

        base_rate = self._account.base_refresh_rate

        for name, dataset in self._datasets.items():
            new_rate = base_rate * self.DATASETS[name]
            dataset.refresh_rate = new_rate

    def get(self, name: str) -> Dataset:
        """Retrieves a dataset"""
        return self._datasets[name]
