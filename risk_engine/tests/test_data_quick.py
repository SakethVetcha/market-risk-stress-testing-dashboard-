from datetime import date
from risk_engine.data import get_price_data, compute_returns

tickers = ["AAPL", "MSFT", "SPY"]
prices = get_price_data(tickers, start="2020-01-01", end=date.today())
print(prices.head())

rets = compute_returns(prices, log=False)
print(rets.head())
print(rets.describe())
