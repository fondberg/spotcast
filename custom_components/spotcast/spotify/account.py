"""Module for the spotify accout class"""


class SpotifyAccount:

    def __init__(
            self,
            sp_dc: str,
            sp_key: str,
    ):
        self._sp_dc = sp_dc
        self._sp_key = sp_key
        self._access_key = None
        self._token_expires = None
