# Market Risk & Stress Testing Dashboard

An interactive Streamlit dashboard to analyze the market risk of equity/ETF portfolios — across both **US/global** and **Indian (NSE)** markets.
It computes key risk metrics (volatility, drawdowns, Value at Risk, Expected Shortfall via three different methodologies), visualizes portfolio vs benchmark performance, tracks rolling beta and correlation per asset, and runs custom stress tests and crisis-window analyses.

> Originally built as a US-market risk dashboard; extended with NIFTY/NSE support, rolling beta, Monte Carlo simulation, and a per-asset stress testing engine to apply it to personal Indian-equity trading and CFA-level risk concepts.

---

## Features

- **Multi-market portfolio construction**
  - Toggle between **US / Global** and **India (NSE)** markets.
  - In NSE mode, plain tickers (`RELIANCE`, `TCS`, `HDFCBANK`) are automatically mapped to Yahoo Finance's NSE format (`RELIANCE.NS`), and **NIFTY 50 / Bank Nifty / Sensex** become available as benchmark options.
  - Load historical prices for user-selected tickers using `yfinance`.
  - Convert prices to daily returns and combine assets into a weighted portfolio.
  - Compute summary stats: daily/annualized volatility and maximum drawdown.

- **Risk metrics — three VaR/ES methodologies side by side**
  - **Historical VaR/ES** — derived directly from the empirical return distribution.
  - **Parametric VaR** — variance–covariance method assuming normally distributed returns.
  - **Monte Carlo VaR/ES** — simulates 10,000 hypothetical daily portfolio outcomes from the assets' historical mean/covariance structure, then reads off VaR/ES from the simulated distribution. Includes a histogram of the simulated return distribution.
  - All available at a configurable confidence level (e.g., 95%, 99%).

- **Time-varying risk relative to the market**
  - Rolling correlation between portfolio returns and a chosen benchmark.
  - **Rolling beta per individual asset** vs the benchmark, so you can see how each holding's market sensitivity shifts over time rather than relying on one static average.

- **Performance visualization**
  - Portfolio vs benchmark equity curves (cumulative return since start date).
  - Clean charts built directly in Streamlit.

- **Stress testing & crisis analysis**
  - **Custom per-asset stress test** — shock each holding by a different amount to model asymmetric scenarios (e.g. "IT drops harder than banking"), rather than one uniform shock across the whole portfolio.
  - Historical crisis window (COVID 2020): slices returns into the Feb–Apr 2020 crash window and recomputes drawdown, VaR, and ES to show real behavior under stress.

---

## Tech Stack

- **Python** – core data handling and quantitative logic.
- **Pandas / NumPy** – time-series processing, portfolio returns, volatility, drawdown, and Monte Carlo simulation.
- **SciPy** – normal distribution quantiles for parametric VaR.
- **yfinance** – download historical OHLCV price data from Yahoo Finance (US and NSE-listed instruments).
- **Streamlit** – web UI for inputs, charts, and interactive analysis.

---

## Project Structure

```text
market-risk-dashboard/
├─ app/
│  └─ main.py          # Streamlit app (UI + wiring to risk engine)
├─ risk_engine/
│  ├─ __init__.py
│  ├─ data.py           # Data download, return calculations, NSE ticker normalization
│  ├─ portfolio.py      # Portfolio returns + summary stats (vol, drawdown)
│  ├─ rolling.py        # Rolling correlation + rolling beta (single-asset & multi-asset)
│  ├─ var.py            # Historical, parametric, and Monte Carlo VaR/ES
│  ├─ scenario.py        # (legacy) uniform shock helper
│  ├─ crisis.py          # Crisis-window (COVID 2020) metrics
│  └─ tests/             # Quick scripts to test each module
└─ README.md
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/<your-username>/market-risk-dashboard.git
cd market-risk-dashboard
```

### 2. Create a virtual environment and install dependencies

```bash
python -m venv .venv
# Windows
.\.venv\Scripts\Activate
# Linux / macOS
source .venv/bin/activate

pip install streamlit pandas numpy yfinance scipy
```

### 3. Run the Streamlit app

```bash
streamlit run app/main.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

---

## How to Use

1. Choose your market: **US / Global** or **India (NSE)**.
2. Enter tickers (comma-separated) — e.g. `AAPL,MSFT,SPY` or `RELIANCE,TCS,HDFCBANK`.
3. Choose a start and end date for historical data.
4. Provide portfolio weights in the text area, one per line, e.g.:
   ```text
   RELIANCE:0.4
   TCS:0.3
   HDFCBANK:0.3
   ```
5. Select a benchmark ticker (SPY, or NIFTY 50 / Bank Nifty / Sensex in NSE mode) and pick a VaR confidence level.
6. Click **Run analysis** to:
   - See portfolio vs benchmark equity curves.
   - View volatility, drawdown, and VaR/ES across all three methodologies (Historical, Parametric, Monte Carlo), including the simulated return distribution.
   - Inspect rolling correlation and rolling beta per asset vs the benchmark.
   - Run a custom per-asset stress test and view COVID-window crisis metrics.

---

## Possible Extensions

- Support FX pairs or other asset classes.
- GARCH-based volatility forecasting for time-varying VaR/ES.
- Fatter-tailed (Student's-t) Monte Carlo simulation instead of normal returns.
- Deploy on Streamlit Community Cloud or another hosting platform.

---

