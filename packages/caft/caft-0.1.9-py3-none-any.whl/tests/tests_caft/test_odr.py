"""Test equation regressors."""

import numpy as np
import pytest
import sympy as sp

from caft.odr import ODRegressor, SympyODRegressor


def sympy_approx_equals(eq1, eq2):
    """Check if two sympy equations are equal. Either an exact match, sp.solve
    returns empty list, or has root 0 in solved list.

    """
    solved_eq = sp.solve(eq1 - eq2)
    if (0 in solved_eq) | (solved_eq == []):
        return True
    else:
        return False


def test_SympyODRegressor():
    """Test sympy function regressor."""
    sodr = SympyODRegressor("a*x**2 + b", beta0={"a": 3, "b": 5})
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


def test_odregressor():
    """Test odr regressor."""
    odr = ODRegressor(degree=2, wrt="s")
    X = np.array([1, 2, 3, 4, 5, 6, 7, 8, 9]).reshape(-1, 1)
    y = (5 * X**2) + (2 * X) + 10
    odr.fit(X, y)
    y_pred = odr.predict(X)
    wrt = sp.Symbol("s")

    check_sp_equation = (
        odr.beta[2] * wrt**2 + (odr.beta[1] * wrt) + odr.beta[0]
    )

    assert odr.beta == pytest.approx([10, 2, 5], rel=1e-3)
    assert odr.sp_equation == check_sp_equation
    assert odr.wrt_symbol == sp.Symbol("s")
    assert y_pred == pytest.approx(y.reshape(-1), rel=1e-3)
