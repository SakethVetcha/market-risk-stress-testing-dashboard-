from datetime import date
from risk_engine.data import get_price_data, compute_returns
from risk_engine.portfolio import portfolio_returns
from risk_engine.rolling import rolling_corr

tickers = ["AAPL", "MSFT", "SPY"]
weights = {"AAPL": 0.3, "MSFT": 0.3, "SPY": 0.4}
benchmark = "SPY"

prices = get_price_data(tickers, start="2020-01-01", end=date.today())
rets = compute_returns(prices, log=False)

port_ret = portfolio_returns(rets, weights)
bench_ret = rets[benchmark]

roll_corr = rolling_corr(port_ret, bench_ret, window=60)
print(roll_corr.tail())
