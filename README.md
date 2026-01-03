# Market Risk & Stress Testing Dashboard

An interactive Streamlit dashboard to analyze the market risk of equity/ETF portfolios.  
It computes key risk metrics (volatility, drawdowns, Value at Risk, Expected Shortfall), visualizes portfolio vs benchmark performance, and runs simple stress tests and crisis‑window analyses.

---

## Features

- **Portfolio construction**
  - Load historical prices for user‑selected tickers using `yfinance` (equities, ETFs, or indices).
  - Convert prices to daily returns and combine assets into a weighted portfolio.
  - Compute summary stats: daily/annualized volatility and maximum drawdown.

- **Risk metrics**
  - Historical Value at Risk (VaR) at configurable confidence levels (e.g., 95%, 99%).
  - Parametric (variance–covariance) VaR assuming normal returns using SciPy.
  - Historical Expected Shortfall (CVaR) as the average loss beyond VaR.

- **Time‑varying correlation**
  - Rolling correlation between portfolio returns and a chosen benchmark index.
  - Helps visualize regime changes when correlation spikes during crises.

- **Performance visualization**
  - Portfolio vs benchmark equity curves (cumulative return since start date).
  - Simple, clean charts built directly in Streamlit.

- **Stress testing & crisis analysis**
  - Uniform shock scenario: “What if the market drops X% in a day?” → approximate portfolio P&L for a user‑selected shock.
  - Historical crisis window (COVID‑like): slice returns into a fixed 2020 crash window and recompute drawdowns, VaR, and ES to show behavior under stress.

---

## Tech Stack

- **Python** – core data handling and quantitative logic.
- **Pandas / NumPy** – time‑series processing, portfolio returns, volatility, and drawdown calculations.
- **SciPy** – normal distribution quantiles for parametric VaR.
- **yfinance** – download historical OHLCV price data from Yahoo Finance.
- **Streamlit** – web UI for inputs, charts, and interactive analysis.

---

## Project Structure

```text
market-risk-dashboard/
├─ app/
│  └─ main.py          # Streamlit app (UI + wiring to risk engine)
├─ risk_engine/
│  ├─ __init__.py
│  ├─ data.py          # Data download + return calculations
│  ├─ portfolio.py     # Portfolio returns + summary stats (vol, drawdown)
│  ├─ rolling.py       # Rolling correlation helper
│  ├─ var.py           # Historical & parametric VaR, Expected Shortfall
│  ├─ scenario.py      # Simple uniform shock stress test
│  ├─ crisis.py        # Crisis-window (e.g., COVID 2020) metrics
│  └─ tests/           # Quick scripts to test each module
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

pip install -r requirements.txt  # if you create one
# or install manually:
# pip install pandas numpy yfinance streamlit scipy plotly
```

### 3. Run the Streamlit app

```bash
streamlit run app/main.py
```

Open the local URL shown in the terminal (usually `http://localhost:8501`).

---

## How to Use

1. Enter tickers (comma‑separated), e.g. `AAPL, MSFT, SPY`.  
2. Choose a start and end date for historical data.  
3. Provide portfolio weights in the text area, one per line, e.g.:  
   ```text
   AAPL:0.3
   MSFT:0.3
   SPY:0.4
   ```  
4. Select a benchmark ticker from the dropdown and pick a VaR confidence level.  
5. Click **Run analysis** to:
   - See portfolio vs benchmark equity curves.
   - View volatility, drawdown, VaR, and ES.
   - Inspect rolling correlation with the benchmark.
   - Run a one‑day shock scenario and view COVID‑window metrics.

---

## Possible Extensions

- Add rolling beta per asset vs benchmark.  
- Support FX pairs or other asset classes.  
- Add Monte Carlo or GARCH‑based VaR/ES models.  
- Deploy on Streamlit Community Cloud or another hosting platform.

---


