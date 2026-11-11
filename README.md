# Apple Stock Risk, Returns & Strategy Analysis

A modular Python project for analysing Apple's (AAPL) historical stock returns and risk, then evaluating a 20/50-day moving-average strategy against a buy-and-hold benchmark.

The project separates reusable calculations from the notebook used to explore, visualize, and communicate results.

## Project structure

```text
.
├── src/
│   └── stock_analysis/
│       ├── __init__.py
│       ├── data_loader.py
│       ├── metrics.py
│       ├── strategy.py
│       └── backtester.py
├── notebooks/
│   └── analysis.ipynb
├── tests/
│   ├── test_metrics.py
│   ├── test_strategy.py
│   └── test_backtester.py
├── .python-version
├── .gitignore
├── pyproject.toml
├── requirements.txt
├── uv.lock
└── README.md
```

## What it does

- Downloads adjusted historical AAPL prices with `yfinance`.
- Calculates daily and cumulative returns.
- Measures CAGR, annualized volatility, maximum drawdown, and Sharpe ratio.
- Generates 20-day and 50-day moving averages.
- Uses lagged positions to avoid same-day look-ahead bias.
- Backtests a long/cash strategy and charges configurable transaction costs.
- Compares the strategy with buy-and-hold.
- Uses a chronological train/test split and reports out-of-sample performance.
- Visualizes price trends, cumulative performance, and drawdowns.

## Setup with uv

Install [uv](https://docs.astral.sh/uv/) if it is not already installed.

From the repository root:

```bash
uv sync --group dev
```

This creates the project environment, resolves dependencies, writes `uv.lock`, and installs runtime and development dependencies. The archive does not include a fabricated lockfile: dependency resolution requires access to the package index, which was unavailable while preparing this archive.

Activate the environment if desired:

```bash
# Windows PowerShell
.venv\Scripts\Activate.ps1

# macOS / Linux
source .venv/bin/activate
```

## Run the analysis

Launch Jupyter:

```bash
uv run jupyter lab
```

Open `notebooks/analysis.ipynb` and run the cells from top to bottom.

The notebook downloads current historical data when executed, so results can differ from previously recorded results as market data and the selected period change.

## Use the package from Python

```python
from stock_analysis import load_stock_data, run_backtest

prices = load_stock_data("AAPL", period="5y")
backtest = run_backtest(
    prices,
    fast_window=20,
    slow_window=50,
    transaction_cost=0.001,
    train_fraction=0.70,
)

print(backtest["metrics"]["test_strategy"])
print(backtest["metrics"]["test_buy_and_hold"])
```

## Module responsibilities

| Module | Responsibility |
|---|---|
| `data_loader.py` | Fetches adjusted price history and computes daily returns. |
| `metrics.py` | Provides reusable return and risk metrics. |
| `strategy.py` | Computes moving averages, signals, and lagged positions. |
| `backtester.py` | Applies positions, transaction costs, benchmark comparison, and chronological test split. |

### Timing and backtesting assumptions

- Prices are downloaded with `auto_adjust=True`, so adjusted OHLC prices are used.
- A signal is calculated using the close available at that observation.
- The position is shifted by one observation before it is applied to close-to-close returns.
- Transaction costs are charged on absolute position changes. The configured rate is a one-way cost per unit of position turnover.
- The test period is the final fraction of the chronological dataset. Moving averages are calculated using historical observations available up to each date, including the pre-test warm-up period.
- The test set should not be used to repeatedly tune strategy parameters. If parameters are selected after reviewing test results, the test is no longer a clean out-of-sample evaluation.

## Run tests

```bash
uv run pytest
```

## Key interpretation

A moving-average strategy should not be considered successful merely because it produces a positive return. Its results should be assessed against a benchmark over the same dates, after transaction costs, and on data that was not used to choose the strategy parameters.

The notebook is intended to report the metrics produced by the current data run rather than hard-code old performance figures. Historical results can change as the downloaded period and market data change.

## Limitations

- The analysis focuses on one security, AAPL.
- The strategy is long/cash and does not model short selling, leverage, slippage, taxes, or market impact.
- The fixed transaction-cost assumption is a simplified estimate.
- A single chronological holdout provides only one out-of-sample period.
- Historical performance does not guarantee future results.

## Disclaimer

This project is for educational and research purposes only. It is not financial advice.
