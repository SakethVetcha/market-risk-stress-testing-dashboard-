import yfinance as yf
import pandas as pd
import numpy as np

def get_price_data(tickers, start, end):
    """
    Download Adjusted Close prices for a list of tickers
    between start and end dates (YYYY-MM-DD or date objects).
    """
    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=False  # keep Close and Adj Close separate
    )
    # Use Adjusted Close if available, else fall back to Close
    if "Adj Close" in data.columns:
        prices = data["Adj Close"]
    else:
        prices = data["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame()
    return prices.dropna()
def compute_returns(price_df, log=False):
    """
    Compute daily returns from price data.
    If log=True, use log returns; else simple percentage returns.
    """
    simple_ret = price_df.pct_change().dropna()  # (P_t - P_{t-1}) / P_{t-1}
    if not log:
        return simple_ret
    # log returns: ln(P_t / P_{t-1})
    log_ret = np.log(price_df / price_df.shift(1)).dropna()
    return log_ret
