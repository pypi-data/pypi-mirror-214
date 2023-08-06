"""Test the affine transform module"""

import numpy as np
import pytest
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model import LinearRegression

from caft.affine import ContinuousAffineFeatureTransformer
from caft.odr import SympyODRegressor
from caft.regressors import SympyRegressor


def test_ConstantAffineFeatureTransformer_outputs():
    """Test the outputs of the CAFT are correct."""
    X = np.linspace(0.8, 1.0, 100).reshape(-1, 1)
    y = (X * 5 + 3).reshape(-1)

    sodr = SympyODRegressor()
    caft = ContinuousAffineFeatureTransformer(sodr)
    caft.fit(X, y)

    assert hasattr(caft, "regressor_")
    assert hasattr(caft.regressor_, "coefs_")

    X_t, y_t = caft.transform(X, y)
    assert X_t.shape == X.shape
    assert y_t.shape == y.shape


@pytest.mark.parametrize(
    ("estimator"),
    (
        pytest.param(SympyODRegressor(), id="SympyODRegressor"),
        pytest.param(SympyRegressor(), id="SympyRegressor"),
        pytest.param(LinearRegression(), id="LinearRegression"),
        pytest.param(RandomForestRegressor(), id="RandomForestRegressor"),
        pytest.param(GaussianProcessRegressor(), id="GaussianProcessRegressor"),
    ),
)
def test_ConstantAffineFeatureTransformer_estimators(estimator):
    "Test other sklearn estimators are compatible with CAFT."
    X = np.linspace(0.8, 1.0, 100).reshape(-1, 1)
    y = (X * 5 + 3).reshape(-1)

    est = estimator
    caft = ContinuousAffineFeatureTransformer(est)
    caft.fit(X, y)
    X_t, y_t = caft.transform(X, y)
    assert y_t.shape == y.shape
