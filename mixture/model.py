
import numpy as np
from . import pricing

class MixtureLognormalModel:
    def __init__(self, n_components):
        self.n_components = n_components
        self.weights = None  # shape (n_expiries, n_components)
        self.sigmas = None   # shape (n_expiries, n_components)

    def price_and_greeks(self, S0, Ks, Ts, r, q, b, is_call=True, cash_divs=None):
        return pricing.mixture_price_and_greeks(
            np.asarray(Ks, dtype=np.float64),
            np.asarray(Ts, dtype=np.float64),
            float(S0),
            np.asarray(r, dtype=np.float64),
            np.asarray(q, dtype=np.float64),
            np.asarray(b, dtype=np.float64),
            np.asarray(self.weights, dtype=np.float64),
            np.asarray(self.sigmas, dtype=np.float64),
            is_call,
            np.asarray(cash_divs, dtype=np.float64) if cash_divs is not None else np.zeros((0, 2))
        )

    def fit_to_prices(self, market_prices, Ks, Ts, S0, r, q, b, is_call=True, cash_divs=None):
        n_T, n_K = market_prices.shape
        N = self.n_components

        def pack_params(weights, sigmas):
            return np.hstack([weights.ravel(), sigmas.ravel()])

        def unpack_params(params):
            weights = params[:n_T*N].reshape(n_T, N)
            sigmas = params[n_T*N:].reshape(n_T, N)
            weights = np.clip(weights, 1e-6, 1.0)
            weights /= weights.sum(axis=1, keepdims=True)
            sigmas = np.clip(sigmas, 1e-4, 5.0)
            return weights, sigmas

        def objective(params):
            weights, sigmas = unpack_params(params)
            self.set_params(weights, sigmas)
            model_prices, _ = self.price_and_greeks(S0, Ks, Ts, r, q, b, is_call, cash_divs)
            return np.mean((model_prices - market_prices)**2)

        init_weights = np.full((n_T, N), 1.0 / N)
        init_sigmas = np.full((n_T, N), 0.2)
        init_params = pack_params(init_weights, init_sigmas)

        from scipy.optimize import minimize
        result = minimize(objective, init_params, method='L-BFGS-B')

        if result.success:
            weights, sigmas = unpack_params(result.x)
            self.set_params(weights, sigmas)
        else:
            raise RuntimeError("Optimization failed: " + result.message)

    def set_params(self, weights, sigmas):
        self.weights = np.asarray(weights, dtype=np.float64)
        self.sigmas = np.asarray(sigmas, dtype=np.float64)
