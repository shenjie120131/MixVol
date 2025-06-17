
import numpy as np
from mixture.pricing import mixture_price_and_greeks

def implied_vol(price, S0, K, T, is_call=True, r=0.0, q=0.0, b=0.0, cash_divs=None, weights=None, sigmas=None):
    r = np.atleast_1d(r)
    q = np.atleast_1d(q)
    b = np.atleast_1d(b)
    if cash_divs is None:
        cash_divs = np.zeros((0, 2))
    else:
        cash_divs = np.atleast_2d(np.asarray(cash_divs, dtype=np.float64))

    if weights is None:
        weights = np.array([[1.0]])
    if sigmas is None:
        sigmas = np.array([[0.2]])

    def objective(sigma):
        px, _ = mixture_price_and_greeks(
            np.array([K]),
            np.array([T]),
            S0,
            r,
            q,
            b,
            np.array(weights),
            np.array([[sigma]]),
            is_call,
            cash_divs
        )
        return px[0, 0] - price

    from scipy.optimize import brentq
    try:
        iv = brentq(objective, 1e-4, 5.0)
    except:
        iv = np.nan
    return iv
