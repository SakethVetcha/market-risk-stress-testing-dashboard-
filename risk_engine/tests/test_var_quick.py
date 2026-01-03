from datetime import date
from risk_engine.data import get_price_data, compute_returns
from risk_engine.portfolio import portfolio_returns
from risk_engine.var import historical_var, historical_es, parametric_var

tickers = ["AAPL", "MSFT", "SPY"]
weights = {"AAPL": 0.3, "MSFT": 0.3, "SPY": 0.4}

prices = get_price_data(tickers, start="2020-01-01", end=date.today())
rets = compute_returns(prices, log=False)

port_ret = portfolio_returns(rets, weights)

alpha = 0.95
print("Hist VaR:", historical_var(port_ret, alpha))
print("Hist ES :", historical_es(port_ret, alpha))
print("Param VaR:", parametric_var(port_ret, alpha))
