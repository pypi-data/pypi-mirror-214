"""Test regressors module."""

import numpy as np
import pytest
import sympy as sp

from caft.regressors import SympyRegressor


def test_SympyRegressor():
    """Test sympy function regressor."""
    sodr = SympyRegressor("a*x**2 + b", beta0={"a": 3, "b": 5})
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
    y = (5 * X**2 + 10).reshape(-1)
    sodr.fit(X, y)
    y_pred = sodr.predict(X)
    wrt = sp.Symbol("x")

    check_sp_equation = sodr.beta[0] * wrt**2 + sodr.beta[1]

    assert sodr.beta == pytest.approx([5, 10], rel=1e-3)
    assert sodr.sp_equation == check_sp_equation
    assert sodr.wrt_symbol == sp.Symbol("x")
    assert y_pred == pytest.approx(y.reshape(-1), rel=1e-3)
