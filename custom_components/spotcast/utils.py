"""Generic utility functions for spotcast

Functions:
    - valid_country_code
"""

from voluptuous import Invalid


def valid_country_code(value: str) -> bool:
    """Validates if a country code provided is valid"""

    if value is None:
        return None

    if not isinstance(value, str):
        raise Invalid("Country Code must be a string")

    if len(value) != 2:
        raise Invalid("Country code must be a 2 character code")

    return value.upper()
