"""Module for the dataset class

Classes:
    - Dataset
"""

from asyncio import Lock
from time import time

from custom_components.spotcast.spotify.exceptions import ExpiredDatasetError
from custom_components.spotcast.utils import copy_to_dict


class Dataset:
    """A dataset that contain a cache and a validation for when the
    data expires

    Attributes:
        - name(str): the name of the dataset
        - refresh_rate(int): the rate at which the dataset needs to
            refresh
        - can_expire(bool): Indicate if the dataset can return data if
            expired
        - expires_at(int): the time (in second) when the dataset will
            be deemed expired
        - lock(Lock): the async lock for the dataset

    Properties:
        - is_expired(bool): True if the dataset is currently expired
        - data(list|dict): the data contained in the dataset

    Methods:
        - update
    """

    def __init__(
            self,
            name: str,
            refresh_rate: int = 30,
            can_expire: bool = False
    ):
        """Constructor for a dataset instance

        Args:
            - name(str): the name of the dataset
            - refresh_rate(int, optional): the duration afteer which
                the dataset is deemed expired. Defaults to 30
            - can_expire(bool, optional): The dataset can return data
                even if expired if set to True. Defaults to False
        """
        self.name = name
        self.refresh_rate = refresh_rate
        self.can_expire = can_expire
        self._data: list | dict | None = None
        self.expires_at = 0
        self.lock = Lock()

    def is_expired(self, strict: bool = True) -> bool:
        """Returns True if the dataset is past is cached time

        Args:
            - strict(bool, optional): In strict mode, will return
            expired as soon as the current reported time is passed the
            expires_at. In non-strict mode, a small buffer is added.
            Defaults to strict.
        """

        if strict:
            expires_at = self.expires_at
        else:
            expires_at = self.expires_at + 2

        return time() > expires_at or self._data is None

    @property
    def data(self) -> list | dict:
        """Returns the data from the dataset or raises an error if
        expired

        Raises:
            - ExpiredDatasetError: raised if the dataset is expired
                unless the can_expire flag is set to True
        """
        if self.is_expired(strict=False) and not self.can_expire:
            raise ExpiredDatasetError(f"The {self.name} dataset is expired")

        return copy_to_dict(self._data)

    def update(self, data: list | dict):
        """Updates the dataset with new data"""
        self._data = data
        self.expires_at = time() + self.refresh_rate
