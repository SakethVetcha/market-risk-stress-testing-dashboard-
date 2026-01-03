import numpy as np
import pandas as pd
from scipy.stats import norm

def historical_var(returns: pd.Series, alpha: float = 0.95) -> float:
    q = np.quantile(returns, 1 - alpha)
    return -q

def historical_es(returns: pd.Series, alpha: float = 0.95) -> float:
    q = np.quantile(returns, 1 - alpha)
    tail = returns[returns <= q]
    return -tail.mean()

def parametric_var(returns: pd.Series, alpha: float = 0.95) -> float:
    mu = returns.mean()
    sigma = returns.std()
    z = norm.ppf(1 - alpha)
    return -(mu + z * sigma)
