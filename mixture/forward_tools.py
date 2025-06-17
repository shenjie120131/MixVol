
import numpy as np

def interpolate_curve(times, values, target_time):
    if target_time <= times[0]:
        return values[0]
    if target_time >= times[-1]:
        return values[-1]
    return np.interp(target_time, times, values)

def discount_cash_dividends(cash_divs, r_curve, b_curve, T_curve, expiry):
    if len(cash_divs) == 0:
        return 0.0
    total = 0.0
    for t, amt in cash_divs:
        if t < expiry:
            r = interpolate_curve(T_curve, r_curve, t)
            b = interpolate_curve(T_curve, b_curve, t)
            total += amt * np.exp(-(r - b) * t)
    return total
