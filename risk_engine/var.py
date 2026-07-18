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

def monte_carlo_var(returns_df, weights, alpha: float = 0.95, n_sims: int = 10000):
    """
    Monte Carlo VaR/ES: simulate n_sims possible daily portfolio returns using
    the historical mean/covariance of the assets, then read off VaR/ES from
    the simulated distribution instead of a formula or raw historical data.

    returns_df: DataFrame of asset returns (columns = tickers)
    weights: dict of {ticker: weight}
    Returns: (var, es, sim_portfolio_returns) — the last one is for plotting.
    """
    tickers = list(returns_df.columns)
    mu = returns_df.mean().values
    cov = returns_df.cov().values
    w = np.array([weights[t] for t in tickers])

    # Simulate n_sims possible daily return vectors, respecting the real
    # correlations between assets (multivariate_normal handles that for us)
    sim_returns = np.random.multivariate_normal(mu, cov, size=n_sims)

    # Each simulated day's portfolio return = weighted sum across assets
    sim_portfolio_returns = sim_returns @ w

    var = -np.quantile(sim_portfolio_returns, 1 - alpha)
    tail = sim_portfolio_returns[sim_portfolio_returns <= -var]
    es = -tail.mean() if len(tail) > 0 else var
    return var, es, sim_portfolio_returns