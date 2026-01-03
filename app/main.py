import os
import sys
from datetime import date

import streamlit as st

# Make sure Python can see the project root so `risk_engine` is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from risk_engine.crisis import crisis_metrics
from risk_engine.data import get_price_data, compute_returns
from risk_engine.portfolio import portfolio_returns, summary_stats
from risk_engine.var import historical_var, historical_es, parametric_var
from risk_engine.rolling import rolling_corr
from risk_engine.scenario import uniform_shock_pnl

st.title("Market Risk & Stress Testing Dashboard")

# --- Inputs ---
tickers_input = st.text_input("Tickers (comma-separated)", "AAPL,MSFT,SPY")
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]

start = st.date_input("Start date", date(2020, 1, 1))
end = st.date_input("End date", date.today())

weights_input = st.text_area(
    "Weights (ticker:weight per line)",
    "AAPL:0.3\nMSFT:0.3\nSPY:0.4",
)

weights = {}
for line in weights_input.splitlines():
    if ":" in line:
        t, w = line.split(":")
        weights[t.strip().upper()] = float(w)

if not tickers:
    st.stop()

benchmark = st.selectbox("Benchmark ticker", tickers)

alpha = st.slider("VaR / ES confidence level", 0.90, 0.99, 0.95, 0.01)

if st.button("Run analysis"):
    # --- Data & returns ---
    prices = get_price_data(tickers, start, end)
    rets = compute_returns(prices, log=False)

    # --- Portfolio series ---
    port_ret = portfolio_returns(rets, weights)
    stats = summary_stats(port_ret)

    st.subheader("Summary statistics")
    st.write(stats)

    # --- Portfolio vs benchmark equity curves ---
    bench_ret = rets[benchmark]

    cum_port = (1 + port_ret).cumprod()
    cum_port.name = "Portfolio"

    cum_bench = (1 + bench_ret).cumprod()
    cum_bench.name = benchmark

    equity_df = cum_port.to_frame().join(cum_bench)

    st.subheader("Portfolio vs benchmark (equity curves)")
    st.line_chart(equity_df)
    
    st.subheader("Crisis window analysis (COVID 2020)")

    crisis_start = "2020-02-15"
    crisis_end = "2020-04-15"

    crisis_stats = crisis_metrics(rets, weights, crisis_start, crisis_end, alpha)

    st.write(
        {
            "Days in window": crisis_stats["n_days"],
            "Crisis max drawdown": crisis_stats["max_drawdown"],
            "Crisis hist VaR": crisis_stats["hist_var"],
            "Crisis hist ES": crisis_stats["hist_es"],
        }
    )

    # --- VaR / ES ---
    h_var = historical_var(port_ret, alpha)
    h_es = historical_es(port_ret, alpha)
    p_var = parametric_var(port_ret, alpha)

    st.subheader("VaR / ES")
    st.write(
        {
            "Historical VaR": h_var,
            "Historical ES": h_es,
            "Parametric VaR": p_var,
        }
    )

    # --- Rolling correlation vs benchmark ---
    roll_corr = rolling_corr(port_ret, bench_ret, window=60)
    st.subheader("Rolling correlation vs benchmark (60D)")
    st.line_chart(roll_corr)

    # --- Simple stress test ---
    st.subheader("Simple stress test")

    shock_pct = st.slider("Market shock (%)", -15.0, 0.0, -5.0, 0.5)
    shock_decimal = shock_pct / 100.0

    stress_pnl = uniform_shock_pnl(weights, shock_decimal)
    st.write(f"Approx portfolio P&L for {shock_pct}% uniform shock: {stress_pnl:.4f}")
