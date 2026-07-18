import os
import sys
from datetime import date
import pandas as pd
import streamlit as st
import numpy as np

# Make sure Python can see the project root so `risk_engine` is importable
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from risk_engine.crisis import crisis_metrics
from risk_engine.data import get_price_data, compute_returns, normalize_nse_tickers, NSE_INDEX_TICKERS
from risk_engine.portfolio import portfolio_returns, summary_stats
from risk_engine.var import historical_var, historical_es, parametric_var, monte_carlo_var
from risk_engine.rolling import rolling_corr, rolling_beta_multi

st.title("Market Risk & Stress Testing Dashboard")

# --- Inputs ---
market = st.radio("Market", ["US / Global", "India (NSE)"], horizontal=True)
is_nse = market == "India (NSE)"

tickers_help = "e.g. RELIANCE,TCS,HDFCBANK" if is_nse else "e.g. AAPL,MSFT,SPY"
tickers_input = st.text_input("Tickers (comma-separated)", "AAPL,MSFT,SPY", help=tickers_help)
tickers = [t.strip().upper() for t in tickers_input.split(",") if t.strip()]
tickers = normalize_nse_tickers(tickers, is_nse=is_nse)

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
        wt = normalize_nse_tickers([t.strip().upper()], is_nse=is_nse)[0]
        weights[wt] = float(w)

if not tickers:
    st.stop()

# On NSE, offer the Nifty 50 / Bank Nifty / Sensex indices as extra benchmark
# choices alongside the portfolio's own tickers.
benchmark_choices = tickers + list(NSE_INDEX_TICKERS.values()) if is_nse else tickers
benchmark = st.selectbox("Benchmark ticker", benchmark_choices)

alpha = st.slider("VaR / ES confidence level", 0.90, 0.99, 0.95, 0.01)

if st.button("Run analysis"):
    st.session_state["run"] = True

if st.session_state.get("run"):
    # --- Data & returns ---
    # --- Data & returns ---
    # Benchmark may be an index (e.g. ^NSEI) that isn't one of the portfolio
    # tickers, so make sure it's included in the download too.
    download_list = tickers if benchmark in tickers else tickers + [benchmark]
    prices = get_price_data(download_list, start, end)
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
# --- VaR / ES ---
    h_var = historical_var(port_ret, alpha)
    h_es = historical_es(port_ret, alpha)
    p_var = parametric_var(port_ret, alpha)
    mc_var, mc_es, mc_sims = monte_carlo_var(rets[tickers], weights, alpha, n_sims=10000)

    st.subheader("VaR / ES")
    st.write(
        {
            "Historical VaR": h_var,
            "Historical ES": h_es,
            "Parametric VaR": p_var,
            "Monte Carlo VaR": mc_var,
            "Monte Carlo ES": mc_es,
        }
    )

    st.subheader("Monte Carlo simulated return distribution")
    st.caption(f"{len(mc_sims):,} simulated daily portfolio returns, with VaR/ES cutoff at {alpha:.0%} confidence.")
    counts, bin_edges = np.histogram(mc_sims, bins=50)
    bin_centers = (bin_edges[:-1] + bin_edges[1:]) / 2
    hist_df = pd.DataFrame({"Return": bin_centers.round(4), "Frequency": counts}).set_index("Return")
    st.bar_chart(hist_df)

    # --- Rolling correlation vs benchmark ---
    roll_corr = rolling_corr(port_ret, bench_ret, window=60)
    st.subheader("Rolling correlation vs benchmark (60D)")
    st.line_chart(roll_corr)

    # --- Rolling beta per asset vs benchmark ---
    # Exclude the benchmark itself from the beta chart (its beta vs itself is always 1).
    asset_cols = [t for t in tickers if t != benchmark]
    if asset_cols:
        roll_beta = rolling_beta_multi(rets[asset_cols], bench_ret, window=60)
        st.subheader("Rolling beta per asset vs benchmark (60D)")
        st.line_chart(roll_beta)

    # --- Simple stress test ---
# --- Custom per-asset stress test ---
    st.subheader("Custom stress test")
    st.caption("Shock each asset by a different amount to see how the mix affects P&L.")

    shock_inputs = {}
    for t in tickers:
        shock_inputs[t] = st.slider(
            f"{t} shock (%)", -30.0, 0.0, -5.0, 1.0, key=f"shock_{t}"
        )

    custom_pnl = sum(weights[t] * (shock_inputs[t] / 100.0) for t in tickers)
    st.write(f"Approx portfolio P&L for this scenario: {custom_pnl:.4f}")