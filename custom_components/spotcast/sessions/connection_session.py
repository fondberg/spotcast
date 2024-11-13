"""Module for the abstract class ConnectionSession

Classes:
    - ConnectionSession
"""

from abc import ABC, abstractmethod


class ConnectionSession(ABC):

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
    def is_healthy(self) -> bool:
        """Returns True if the session is able to refresh its token"""
        return self._is_healthy
