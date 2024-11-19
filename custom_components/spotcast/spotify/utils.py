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

        area = image["width"] * image["height"]

        if area > max_area:
            image_url = image["url"]
            max_area = area

    return image_url
