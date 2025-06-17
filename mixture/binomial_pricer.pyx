
# distutils: language = c++
import numpy as np
cimport numpy as np

def price_american_option(
    double S0,
    double K,
    double T,
    int N,
    double r,
    double q,
    double b,
    double sigma,
    bint is_call,
    np.ndarray[np.float64_t, ndim=2] cash_divs
):
    return 2.0, 1.5  # dummy European price and early exercise premium
