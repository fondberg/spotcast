"""Utility functions for interacting with Spotify"""


def select_image_url(images: list[dict]) -> str:
    """Returns the highest resolution image available according to the
    list of images provided

    Args:
        - images(list[dict]): the list of images as returned by a
            Spotify API endpoint. Expected to have a `height`, `width`,
            and `url` key.

    Returns:
        - str: The URL of the highest resolution image
    """
    image_url = None
    max_area = 0

    for image in images:

        width = image.get("width")
        height = image.get("height")

        # assume top image best fit when no size provided
        if any(x is None for x in (width, height)):
            image_url = image["url"]
            break

        area = image["width"] * image["height"]

        if area > max_area:
            image_url = image["url"]
            max_area = area

    return image_url


def url_to_uri(url: str) -> str:
    """converts a url to a spotify uri"""

    # if already a uri skip
    if url.startswith("spotify:"):
        return url

    # remove the protocol section
    url = url.split("://", maxsplit=1)[-1]

    # remove query if present
    url = url.rsplit("?", maxsplit=1)[0]

    # split items on slashes
    elems = url.split('/')

    # replace first item with spotify
    elems[0] = "spotify"

    uri = ":".join(elems)

    return uri
