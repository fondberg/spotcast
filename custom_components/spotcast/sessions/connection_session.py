"""Module for the abstract class ConnectionSession"""

from abc import ABC, abstractmethod


class ConnectionSession(ABC):

    @abstractmethod
    async def async_ensure_token_valid(self):
        """Method that ensures a token is currently valid"""

    @property
    @abstractmethod
    def token(self) -> str:
        """Retrives the token for the session"""
