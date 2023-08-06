"""Equation based regressors."""

import sympy as sp
from scipy.odr import ODR, Data, Model, exponential, multilinear, polynomial
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils import check_array, check_X_y
from sklearn.utils.validation import check_is_fitted


class SympyODRegressor(BaseEstimator, RegressorMixin):
    """Fit a Sympy equation to data using Orthogonal Distance Regression

    Typically used on data that is known to have uncertainty in both the x and
    y variables and when a rough estimate for the function shape is known.

    Parameters
    ----------
    equation : str
        A string that can be parsed by sympy. By default, a linear model.
    beta0 : dict
        A dictionary of initial values for the parameters in the equation. By
        default, linear model parameters, `a=1` and `c=0`.
    wrt : str, optional
        The variable to fit the equation to, by default "x".

    Attributes
    ----------
    sp_equation : sympy expression
        The sympy expression parsed from the equation string.
    wrt_symbol : sympy symbol
        The sympy symbol parsed from the wrt string.
    free_symbols_user : list of sympy symbols
        The sympy symbols parsed from the keys of the beta0 dictionary.
    beta : list of floats
        The fitted parameters for the equation.


    Notes
    -----
    From the implementation point of view, this is a wrapper around
    scipy.odr with a sympy equation parser as an function to optimize.

    Examples
    --------
    >>> import numpy as np
    >>> import sympy as sp
    >>> from caft.equation import SympyFunctionRegressor

    >>> np.random.seed(43)
    >>> X = np.random.normal(0, 1, size=(100, 1)) / 2
    >>> X_noise = (np.random.normal(0, 1, size=(100, 1)) / 5)
    >>> y_noise = (np.random.normal(0, 1, size=(100, 1)) / 5)
    >>> y = (X + X_noise) ** 2 + 10 + y_noise

    >>> equation = "a*x**2 + b"
    >>> sp.parsing.sympy_parser.parse_expr(equation)
    >>> sfr = SympyFunctionRegressor(equation, beta0={"a": 3, "b": 5})
    >>> sfr.fit(X, y)
    >>> y_pred = sfr.predict(X)

    >>> sfr.beta
    array([1.60245274, 9.89329657])...
    """

    def __init__(
        self,
        equation: str = "a*x + c",
        beta0: dict = {"a": 1, "c": 0},
        wrt: str = "x",
    ):
        self.equation = equation
        self.wrt = wrt
        self.beta0 = beta0

    def fit(self, X, y):
        """Fit the sympy equation to the data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values (real numbers in regression).
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

        self.mod = Model(self.odr_function)
        dat = Data(X_, y_)
        self.od = ODR(
            dat,
            self.mod,
            beta0=list(self.beta0.values()),
        )
        self.coefs_ = self.od.run()
        self.beta = self.coefs_.beta
        subs_beta = []
        for s, b in zip(self.free_symbols_user, self.beta):
            subs_beta.append((s, b))
            setattr(self, s.name, b)

        self.subs_beta = subs_beta
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

    def odr_function(self, beta, x):
        """The function to optimize with scipy.odr."""
        odr_fx_subs = self.sp_equation.subs(
            [(s, b) for s, b in zip(self.free_symbols_user, beta)]
        )
        return sp.lambdify(self.wrt_symbol, odr_fx_subs)(x)


class ODRegressor(BaseEstimator, RegressorMixin):
    """Fit a scipy Orthogonal Distance Regressor in a sklearn style.

    Typically used on data that is known to have uncertainty in both the x and
    y variables and no estimate for the function shape is needed.

    Parameters
    ----------
    model_type : str
        The type of model to fit. Can be exponential or polynomial, by
        default `polynomial`. For linear use `degree=1`. See scipy.odr.Model
        for details.
    degree : int, optional
        The degree of the polynomial to fit, by default 3. If model_type is not
        polynomial, this parameter is ignored.
    wrt : str, optional
        The variable to fit the equation with respect to, by default "x".
    """

    def __init__(
        self,
        model_type: str = "polynomial",
        degree: int = 3,
        wrt: str = "x",
    ):
        self.model_type = model_type
        self.wrt = wrt
        self.degree = degree

    def fit(self, X, y):
        """Fit a scipy.odr Model to the data.

        Parameters
        ----------
        X : array-like of shape (n_samples, n_features)
            The training input samples.
        y : array-like of shape (n_samples,)
            The target values (real numbers in regression).
        """
        X_, y_ = check_X_y(X, y)
        X_ = X_[:, 0]

        if self.model_type == "polynomial":
            self.mod = polynomial(self.degree)
        elif self.model_type == "exponential":
            self.mod = exponential()
        elif self.model_type == "multilinear":
            self.mod = multilinear()
        else:
            raise ValueError(
                "model_type must be linear, exponential or polynomial"
            )

        dat = Data(X_, y_)
        self.od = ODR(dat, self.mod)
        self.coefs_ = self.od.run()
        self.beta = self.coefs_.beta

        self.wrt_symbol = sp.Symbol(self.wrt)

        if self.model_type == "polynomial":
            self.sp_equation = sp.Poly.from_list(
                self.beta[::-1], self.wrt_symbol
            ).as_expr()
        elif self.model_type == "exponential":
            self.sp_equation = self.beta[0] + sp.exp(
                self.beta[1] * self.wrt_symbol
            )
        elif self.model_type == "multilinear":
            self.sp_equation = sum(
                [b * self.wrt_symbol**i for i, b in enumerate(self.beta)]
            )
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
