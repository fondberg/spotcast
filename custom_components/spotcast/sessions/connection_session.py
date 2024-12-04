"""Module for the abstract class ConnectionSession

Classes:
    - ConnectionSession
"""

from abc import ABC, abstractmethod


class ConnectionSession(ABC):

    API_ENDPOINT = None

    def __init__(self):
        self._is_healthy = False

    @abstractmethod
    async def async_ensure_token_valid(self):
        """Method that ensures a token is currently valid"""

    @property
    @abstractmethod
    def token(self) -> str:
        """Retrives the token for the session"""

    @property
    @abstractmethod
    def clean_token(self) -> str:
        """returns the currently valid token only, no additional
        information"""

    @property
    def is_healthy(self) -> bool:
        """Returns True if the session is able to refresh its token"""
        return self._is_healthy
