import numpy as np
import pandas as pd

def portfolio_returns(returns_df: pd.DataFrame, weights: dict) -> pd.Series:
    """
    Combine asset returns into a single portfolio return series.

    returns_df: DataFrame with columns = tickers, index = dates
    weights: dict {ticker: weight}, weights should sum ~1
    """
    w = pd.Series(weights).reindex(returns_df.columns).fillna(0).values
    port_ret = returns_df.values @ w  # matrix multiply
    return pd.Series(port_ret, index=returns_df.index, name="portfolio")

def summary_stats(portfolio_ret: pd.Series, trading_days: int = 252) -> dict:
    """
    Compute basic risk/return stats for the portfolio.
    """
    mean_daily = portfolio_ret.mean()
    vol_daily = portfolio_ret.std()
    ann_vol = vol_daily * np.sqrt(trading_days)

    # cumulative wealth curve
    cum = (1 + portfolio_ret).cumprod()
    running_max = cum.cummax()
    drawdown = cum / running_max - 1
    max_dd = drawdown.min()  # most negative value = max drawdown[web:118][web:120]

    return {
        "mean_daily": mean_daily,
        "vol_daily": vol_daily,
        "ann_vol": ann_vol,
        "max_drawdown": max_dd,
    }
