"""Module for the dataset class

Classes:
    - Dataset
"""

from asyncio import Lock
from time import time

from custom_components.spotcast.spotify.exceptions import ExpiredDatasetError


class Dataset:

    def __init__(self, name: str, refresh_rate: int = 30):
        self.name = name
        self.refresh_rate = refresh_rate
        self._data: list | dict | None = None
        self.last_refresh = 0
        self.lock = Lock()

    @property
    def is_expired(self) -> bool:
        """Returns True if the dataset is past is cached time"""
        return (
            time() > self.last_refresh + self.refresh_rate
            or self._data is None
        )

    @property
    def data(self) -> list | dict:
        """Returns the data from the dataset or raises an error if
        expired"""
        if self.is_expired:
            raise ExpiredDatasetError(f"The {self.name} dataset is expired")

        return self._data

    def update(self, data: list | dict):
        self._data = data
        self.last_refresh = time()
