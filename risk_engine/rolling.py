import pandas as pd

def rolling_corr(series_a: pd.Series, series_b: pd.Series, window: int = 60) -> pd.Series:
    """
    Rolling correlation between two return series.

    series_a, series_b: aligned pd.Series (same dates index)
    window: rolling window length in days
    """
    return series_a.rolling(window).corr(series_b)

def rolling_beta(asset_ret: pd.Series, bench_ret: pd.Series, window: int = 60) -> pd.Series:
    """
    Rolling beta of an asset vs a benchmark: beta = Cov(asset, bench) / Var(bench).

    asset_ret, bench_ret: aligned pd.Series (same dates index)
    window: rolling window length in days
    """
    rolling_cov = asset_ret.rolling(window).cov(bench_ret)
    rolling_var = bench_ret.rolling(window).var()
    return rolling_cov / rolling_var

def rolling_beta_multi(returns_df: pd.DataFrame, bench_ret: pd.Series, window: int = 60) -> pd.DataFrame:
    """
    Rolling beta of every column in returns_df vs the same benchmark.

    Returns a DataFrame with one beta column per asset, aligned on date.
    """
    betas = {
        col: rolling_beta(returns_df[col], bench_ret, window)
        for col in returns_df.columns
    }
    return pd.DataFrame(betas)