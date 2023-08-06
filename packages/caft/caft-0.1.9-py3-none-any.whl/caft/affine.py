"""Affine transformation functions."""

import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin, clone
from sklearn.metrics import pairwise_distances_argmin
from sklearn.utils import check_X_y

from caft.utils import check_X_single_feature


def rotate(X, y, grad):
    """Rotate X and y from the normal to the curve to "12 o'clock".

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The training input samples.
    y : array-like of shape (n_samples,)
        The target values.
    grad : array-like of shape (n_features,)
        The normal vector to the curve at the point of interest.

    Returns
    -------
    X_rotated : array-like of shape (n_samples, n_features)
        The rotated X values.
    y_rotated : array-like of shape (n_samples, n_features)
        The rotated y values.
    """
    Xy = np.hstack([X, y])
    theta = np.arctan(grad)
    # fmt: off
    rotate = np.array([
        [np.cos(theta), -np.sin(theta)],
        [np.sin(theta), np.cos(theta)]
    ])
    # fmt: on

    rotate = np.transpose(rotate, (2, 0, 1))
    Xy_ = Xy[:, None, :]
    rotated = np.matmul(Xy_, rotate)[:, 0, :]
    return rotated[:, [0]], rotated[:, [1]]


class ContinuousAffineFeatureTransformer(BaseEstimator, TransformerMixin):
    """Transform X and y with respect to the fitted regressor.

    CAFT uses affine transformations on X and y with respect to the fitted
    regressor. That is to say, for each point in X and y, the nearest point on
    the fitted curve is used as the origin for the rotation.

    CAFT attempts to use use these transformations to reveal outliers when
    cleaning data that is known to be noisy in both the X and y.

    Parameters
    ----------
    regressor : sklearn regressor
        A regressor that implements the `fit` and `predict` methods.
    n_grid : int, optional
        The number of points to use in the grid search for the nearest point.
    rotate_y : bool, optional
        Whether to use y-rotation values in the transformation.
    translate_y : bool, optional
        Whether to use y-translation values in the transformation.
    """

    def __init__(
        self, regressor, n_grid=10000, rotate_y=True, translate_y=False
    ):
        self.regressor = regressor
        self.n_grid = n_grid
        self.rotate_y = rotate_y
        self.translate_y = translate_y

    def fit(self, X, y):
        """Fit the regressor to X and y.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        self : object
            Returns self.
        """
        X_, y_ = check_X_y(X, y)
        check_X_single_feature(X_)
        self.regressor_ = clone(self.regressor)
        X_, y_ = self.scale_X_y(X_, y_)
        self.regressor_.fit(X_, y_)
        return self

    def transform(self, X, y):
        """Transform X and y with respect to the fitted regressor.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        X_t : array-like of shape (n_samples, n_features)
            The transformed input samples.
        y_t : array-like of shape (n_samples,)
            The transformed target values.
        """
        X_, y_ = check_X_y(X, y)
        check_X_single_feature(X_)
        y_ = y_.reshape(-1, 1)

        X_ = (X - self._centre_X) / (self._X_range)
        y_ = (y_ - self._centre_y) / (self._y_range)

        X_npoc, y_npoc = self.nearest_point_on_curve(X_, y_)
        X_centred = X_ - X_npoc
        y_centred = y_ - y_npoc
        grad = self.derivative(X_npoc, y_npoc)[0].reshape(-1)
        X_rot, y_rot = rotate(X_centred, y_centred, grad)

        X_ = X_rot + X_npoc

        if self.rotate_y and not self.translate_y:
            y_ = y_rot
        elif self.rotate_y and self.translate_y:
            y_ = y_rot + y_npoc
        elif not self.rotate_y and self.translate_y:
            y_ = y_npoc
        else:
            y_ = y_

        X_t, y_t = self.inverse_scale_X_y(X_.reshape(-1, 1), y_)
        return X_t, y_t.reshape(-1)

    def scale_X_y(self, X, y):
        """Scale X and y to the range [0, 1].

        This assumes that errors in X and y are of the same order of magnitude.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        X_ : array-like of shape (n_samples, n_features)
            The scaled input samples.
        y_ : array-like of shape (n_samples,)
            The scaled target values.
        """
        self._X_min = X.min()
        self._y_min = y.min()
        self._X_max = X.max()
        self._y_max = y.max()
        self._centre_X = (self._X_max + self._X_min) / 2
        self._centre_y = (self._y_max + self._y_min) / 2

        self._X_range = self._X_max - self._X_min
        self._y_range = self._y_max - self._y_min

        X_ = (X - self._centre_X) / (self._X_range)
        y_ = (y - self._centre_y) / (self._y_range)
        return X_, y_

    def inverse_scale_X_y(self, X, y):
        """Inverse scale X and y from the range [0, 1].

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        X_ : array-like of shape (n_samples, n_features)
            The inverse scaled input samples.
        y_ : array-like of shape (n_samples,)
            The inverse scaled target values.
        """
        X_ = (X * self._X_range) + self._centre_X
        if self.translate_y:
            y_ = (y * self._y_range) + self._centre_y
        else:
            y_ = y * self._y_range
        return X_, y_

    def nearest_point_on_curve(self, X, y):
        """Find the nearest point on the fitted curve to each point in X and y.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        X_npoc : array-like of shape (n_samples, n_features)
            The nearest point on the fitted curve to each point in X.
        y_npoc : array-like of shape (n_samples,)
            The nearest point on the fitted curve to each point in y.
        """
        domain_extension = 0.1
        X_domain = np.linspace(
            X.min() - domain_extension, X.max() + domain_extension, self.n_grid
        ).reshape(-1, 1)

        fp = np.hstack(
            [X_domain, self.regressor_.predict(X_domain).reshape(-1, 1)]
        )

        Xy = np.hstack([X, y])
        Xy_nearest_idx = pairwise_distances_argmin(Xy, fp, metric="euclidean")
        return (
            fp[Xy_nearest_idx, 0].reshape(-1, 1),
            fp[Xy_nearest_idx, 1].reshape(-1, 1),
        )

    def derivative(self, X, y):
        """Calculate the derivative of the fitted curve at each point.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values.

        Returns
        -------
        grad : array-like of shape (n_samples,)
            The derivative of the fitted curve at each point.
        """
        # dx = (X.max() - X.min()) / (y.shape[0] - 1)
        return np.gradient(y.reshape(-1), X.reshape(-1))

    def predict_regressor(self, X):
        """Predict using the fitted regressor.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.

        Returns
        -------
        y : array-like of shape (n_samples,)
            The predicted values.
        """
        X_ = (X - self._centre_X) / (self._X_range)
        return self.regressor_.predict(X_) * self._y_range + self._centre_y
