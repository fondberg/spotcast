"""Module for the dataset class

Classes:
    - Dataset
"""

from asyncio import Lock
from time import time
from typing import Callable, Awaitable
from logging import getLogger

LOGGER = getLogger(__name__)


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
            refresh_function: Callable[[], Awaitable],
            refresh_rate: int = 30,
            can_expire: bool = False,
            *args,
            **kwargs,
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
        self._refresh_function = refresh_function
        self.refresh_rate = refresh_rate
        self.can_expire = can_expire
        self._data: list | dict | None = None
        self.expires_at = 0
        self.lock = Lock()
        self.args = args
        self.kwargs = kwargs

    @property
    def is_expired(self) -> bool:
        """Returns True if the dataset is past is cached time"""
        return time() > self.expires_at or self._data is None

    async def async_get(self) -> dict:
        """Retrives the dataset content. Updating it if necessary"""

        async with self.lock:
            if self.is_expired:
                LOGGER.debug("Refreshing %s dataset", self.name)
                self._data = await self._refresh_function(
                    *self.args,
                    **self.kwargs
                )
                self.expires_at = time() + self.refresh_rate
            else:
                LOGGER.debug("Using cached %s dataset", self.name)

        return self._data

    def update(self, data: list | dict):
        """Updates the dataset with new data"""
        self._data = data
        self.expires_at = time() + self.refresh_rate
