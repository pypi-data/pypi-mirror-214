"""Exceptions for the CAFT package."""


class SingleFeatureException(ValueError):
    """Exception for when a single feature 2D array is expected but not given.

    This might include a 1D array, or a 2D array with more than one feature or
    a >=3D array of any size."""

    pass
