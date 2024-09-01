"""Module for the spotify accout class"""

from custom_components.spotcast.spotify import SpotifyToken


class SpotifyAccount:
    """A Spotify Account with the cookies information

    Attributes:
        - country(str): The ISO3166-2 country code for the account
    """

    def __init__(
            self,
            sp_dc: str,
            sp_key: str,
            country: str = None,
    ):
        self._sp_dc = sp_dc
        self._sp_key = sp_key
        self.country = country

        self._token = SpotifyToken(sp_dc=sp_dc, sp_key=sp_key)

    def get_token(self) -> str:
        """Returns a non expired token"""
        return self._token.get(self._sp_dc, self._sp_key)
