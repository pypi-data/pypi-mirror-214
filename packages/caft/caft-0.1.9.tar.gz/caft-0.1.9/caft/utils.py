"""Utils and helpers for CAFT."""

from caft.exceptions import SingleFeatureException


def check_X_single_feature(X):
    """Check that X is 2D with shape (n_samples, 1) to be sklearn compatible.

    Parameters
    ----------
    X : array-like of shape (n_samples, n_features)
        The input samples.

    Returns
    -------
    X : ndarray of shape (n_samples, 1)
        The input samples.
    """
    if X.ndim != 2:
        raise SingleFeatureException(
            f"X must be 2D with shape (n_samples, 1), not {X.ndim}D."
        )
    if X.shape[1] != 1:
        raise SingleFeatureException("X must be 2D with shape (n_samples, 1).")
    else:
        return X[:, [0]]
