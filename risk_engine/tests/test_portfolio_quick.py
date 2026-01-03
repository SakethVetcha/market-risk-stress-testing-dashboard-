from datetime import date
from risk_engine.data import get_price_data, compute_returns
from risk_engine.portfolio import portfolio_returns, summary_stats

tickers = ["AAPL", "MSFT", "SPY"]
weights = {"AAPL": 0.3, "MSFT": 0.3, "SPY": 0.4}

prices = get_price_data(tickers, start="2020-01-01", end=date.today())
rets = compute_returns(prices, log=False)

port_ret = portfolio_returns(rets, weights)
print(port_ret.head())

stats = summary_stats(port_ret)
print(stats)
