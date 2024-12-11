"""Module for the SearchQuery class"""

from custom_components.spotcast.spotify.exceptions import (
    InvalidFilterError,
    InvalidTagsError,
    InvalidItemTypeError,
)


class SearchQuery:

    ALLOWED_FILTERS = (
        "album",
        "artist",
        "track",
        "year",
        "upc",
        "isrc",
        "genre",
    )

    ALLOWED_TAGS = (
        "hipster",
        "new",
    )

    ALLOWED_ITEM_TYPE = (
        "album",
        "artist",
        "playlist",
        "track",
        "show",
        "episode",
        "audiobook",
    )

    def __init__(
            self,
            search: str,
            item_types: str | list[str],
            filters: dict[str, str] = None,
            tags: list[str] = None,
    ):

        filters = {} if filters is None else filters
        tags = [] if tags is None else tags
        item_types = item_types if isinstance(item_types, list) else [
            item_types
        ]

        self.raise_on_invalid_filters(filters)
        self.raise_on_invalid_tags(tags)
        self.raise_on_invalid_item_type(item_types)

        self.search = search
        self.item_types = item_types
        self.filters = filters
        self.tags = tags

    @property
    def query_string(self) -> str:
        """Returns the query string ready for spotify api call"""

        query = self.search

        if len(self.filters) > 0:
            filter_strings = [f"{x}:{y}" for x, y in self.filters.items()]
            query += " " + " ".join(filter_strings)

        if len(self.tags) > 0:
            tags_strings = [f"tag:{x}" for x in self.tags]
            query += " " + " ".join(tags_strings)

        return query

    @property
    def item_types_string(self) -> str:
        """Returns the string for the item_types to search"""
        return ','.join(self.item_types)

    @classmethod
    def raise_on_invalid_item_type(cls, item_types: list[str]):
        """Raises an InvalidItemTypeError if an invalid item time
        was provided"""

        for item_type in item_types:
            if item_type not in cls.ALLOWED_ITEM_TYPE:
                raise InvalidItemTypeError(
                    f"`{item_type}` is not a valid item type. Must be part of "
                    f"{cls.ALLOWED_ITEM_TYPE}"
                )

    @classmethod
    def raise_on_invalid_filters(cls, filters: dict[str, str]):
        """Raises an InvalidFilterError if an invalid filter was
        provided"""
        for key in filters.keys():
            if key not in cls.ALLOWED_FILTERS:
                raise InvalidFilterError(
                    f"`{key}` is not an allowed filter. Must be part of "
                    f"{cls.ALLOWED_FILTERS}"
                )

    @classmethod
    def raise_on_invalid_tags(cls, tags: list[str]):
        """Raises an InvalidTagsError if an invalid tag was provided
        """
        for tag in tags:
            if tag not in cls.ALLOWED_TAGS:
                raise InvalidTagsError(
                    f"`{tag}` is not an allowed tag. Must be part of "
                    f"{cls.ALLOWED_TAGS}"
                )
