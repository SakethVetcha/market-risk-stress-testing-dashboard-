import pandas as pd

def rolling_corr(series_a: pd.Series, series_b: pd.Series, window: int = 60) -> pd.Series:
    """
    Rolling correlation between two return series.

    series_a, series_b: aligned pd.Series (same dates index)
    window: rolling window length in days
    """
    return series_a.rolling(window).corr(series_b)
