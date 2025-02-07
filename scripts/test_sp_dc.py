"""Script to test the sp_dc and sp_key to ensure they are valid for use in Spotcast"""

from asyncio import run
from os import getenv
from argparse import Namespace, ArgumentParser, ArgumentError
from unittest.mock import MagicMock

from custom_components.spotcast.sessions import PrivateSession


def get_args() -> Namespace:

    parser = ArgumentParser("test_sp_dc")

    parser.add_argument(
        "--sp-dc",
        help="Your SP_DC",
        default=getenv("SP_DC")
    )

    parser.add_argument(
        "--sp-key",
        help="Your SP_KEY",
        default=getenv("SP_KEY")
    )

    config = parser.parse_args()

    config_dict = vars(config)

    for key in ("sp_dc", "sp_key"):

        flag = "--" + key.replace("_", "-")
        env_key = key.upper()

        if config_dict[key] is None:
            raise ArgumentError(
                argument=key,
                message=f"{key} is required. Please provide using the `{flag}`"
                f" or using the {env_key} environment variable."
            )

    return config


async def main():

    config = get_args()
    mock_entry = MagicMock()
    mock_entry.data = {
        "internal_api": {
            "sp_dc": config.sp_dc,
            "sp_key": config.sp_key,
        }
    }

    session = PrivateSession(MagicMock(), mock_entry)

    await session.async_ensure_token_valid()

    print("Token Retrieved Successfully")
    print(f"Token: {session.token}")


if __name__ == '__main__':
    run(main())
