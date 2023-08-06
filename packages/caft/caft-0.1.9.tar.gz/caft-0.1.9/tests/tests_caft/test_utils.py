"""Test the utils module."""

import numpy as np
import pytest

from caft.exceptions import SingleFeatureException
from caft.utils import check_X_single_feature


@pytest.mark.parametrize(
    "X_in, X_expected",
    [
        (
            np.array([[1], [2], [3]]),
            np.array([[1], [2], [3]]),
        ),
    ],
)
def test_check_X_single_feature(X_in, X_expected):
    """Test the check_X_single_feature function pass for a simple cases."""
    assert all(check_X_single_feature(X_in) == X_expected)


@pytest.mark.parametrize(
    "X_in, X_expected",
    [
        (np.array([[1, 2, 3]]), SingleFeatureException),
        (np.array([1, 2, 3]), SingleFeatureException),
        (np.array([[1, 2], [3, 4]]), SingleFeatureException),
        (np.array([[[1, 2], [3, 4], [1, 2]]]), SingleFeatureException),
    ],
)
def test_check_X_single_feature_raises(X_in, X_expected):
    """Test the check_X_single_feature function raises errors."""
    with pytest.raises(SingleFeatureException):
        assert check_X_single_feature(X_in) == X_expected
