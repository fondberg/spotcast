"""Module for the dataset class

Classes:
    - Dataset
"""

from asyncio import Lock
from time import time

from custom_components.spotcast.spotify.exceptions import ExpiredDatasetError


class Dataset:

    def __init__(
            self,
            name: str,
            refresh_rate: int = 30,
            can_expire: bool = False
    ):
        self.name = name
        self.refresh_rate = refresh_rate
        self.can_expire = can_expire
        self._data: list | dict | None = None
        self.expires_at = 0
        self.lock = Lock()

    @property
    def is_expired(self) -> bool:
        """Returns True if the dataset is past is cached time"""
        return time() > self.expires_at or self._data is None

    @property
    def data(self) -> list | dict:
        """Returns the data from the dataset or raises an error if
        expired"""
        if self.is_expired and not self.can_expire:
            raise ExpiredDatasetError(f"The {self.name} dataset is expired")

        return self._data

    def update(self, data: list | dict):
        self._data = data
        self.expires_at = time() + self.refresh_rate
