"""Module containing sessions managers for different usecases

Classes:
    - InternalSession
    - OAuth2Session
    - ConnectionSession

Functions:
    - async_get_config_entry_implementation
"""

from custom_components.spotcast.sessions.internal_session import (
    InternalSession
)
from custom_components.spotcast.sessions.oauth2_session import (
    OAuth2Session,
    async_get_config_entry_implementation,
)
from custom_components.spotcast.sessions.connection_session import (
    ConnectionSession
)
