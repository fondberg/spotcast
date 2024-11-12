"""Generic exceptions for spotcast"""


class LowRatioError(Exception):
    """Raised when a best fuzzy match is too low to return a result"""
