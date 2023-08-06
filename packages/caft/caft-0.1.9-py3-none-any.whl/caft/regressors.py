"""Fit functions with Least Squares Regression."""

import sympy as sp
from scipy.optimize import curve_fit
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils import check_array, check_X_y
from sklearn.utils.validation import check_is_fitted


class SympyRegressor(BaseEstimator, RegressorMixin):
    """Fit a Sympy equation to data using Least Squares Regression

    Parameters
    ----------
    equation : str
        A string that can be parsed by sympy. By default, a linear model.
    beta0 : dict
        A dictionary of initial values for the parameters in the equation.
        By default, linear model parameters, `a=1` and `c=0`.
    wrt : str, optional
        The variable to fit the equation to, by default "x".
    """

    def __init__(
        self,
        equation: str = "a*x + c",
        beta0: dict = {"a": 1, "c": 0},
        wrt: str = "x",
    ):
        self.equation = equation
        self.beta0 = beta0
        self.wrt = wrt

    def fit(self, X, y):
        """Fit the equation to the data.

        Parameters
        ----------
        X : array-like
            The independent variable.
        y : array-like
            The dependent variable.

        Returns
        -------
        self : object
            Returns self.
        """
        X_, y_ = check_X_y(X, y)
        X_ = X_[:, 0]

        self.sp_equation = sp.parsing.sympy_parser.parse_expr(self.equation)
        self.wrt_symbol = sp.Symbol(self.wrt)
        free_symbols_auto = self.sp_equation.free_symbols
        self.free_symbols_user = [sp.Symbol(s) for s in self.beta0.keys()] + [
            self.wrt_symbol
        ]

        if free_symbols_auto != set(self.free_symbols_user):
            raise ValueError("beta0 keys must match equation free symbols")

        self.subs_beta0 = [(sp.Symbol(k), v) for k, v in self.beta0.items()]

        def func(x, *beta):
            fx_subs = self.sp_equation.subs(
                [(s, b) for s, b in zip(self.free_symbols_user, beta)]
            )
            return sp.lambdify(self.wrt_symbol, fx_subs)(x).reshape(-1)

        self.beta, self.cov = curve_fit(
            func, X_, y_, p0=list(self.beta0.values())
        )

        self.subs_beta = []
        for s, b in zip(self.free_symbols_user, self.beta):
            self.subs_beta.append((s, b))
            setattr(self, s.name, b)

        self.sp_equation = self.sp_equation.subs(self.subs_beta)
        return self

    def predict(self, X):
        """Predict regression target for X.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The input samples.

        Returns
        -------
        y : ndarray of shape (n_samples,)
            The predicted values.
        """
        check_is_fitted(self, ["beta"])
        X_ = check_array(X)

        return sp.lambdify(self.wrt_symbol, self.sp_equation)(X_).reshape(-1)
