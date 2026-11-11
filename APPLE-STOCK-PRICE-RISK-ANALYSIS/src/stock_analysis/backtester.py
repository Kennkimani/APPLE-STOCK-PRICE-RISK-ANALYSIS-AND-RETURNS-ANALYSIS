"""Backtesting, transaction-cost modeling, and benchmark comparison."""

from __future__ import annotations

import pandas as pd

from .metrics import summarize_returns
from .strategy import generate_moving_average_signals


def run_backtest(
    data: pd.DataFrame,
    fast_window: int = 20,
    slow_window: int = 50,
    transaction_cost: float = 0.001,
    train_fraction: float = 0.70,
    risk_free_rate: float = 0.04,
) -> dict:
    """Run a long/cash moving-average backtest and chronological test split.

    Transaction cost is charged on absolute position changes. The out-of-sample
    slice is taken only after signals/positions are computed chronologically
    over the full price history, allowing the test period to use prior prices
    for moving-average warm-up without looking into future observations.
    """
    if not 0.0 <= transaction_cost < 1.0:
        raise ValueError("transaction_cost must be in [0, 1).")
    if not 0.0 < train_fraction < 1.0:
        raise ValueError("train_fraction must be between 0 and 1.")
    if "Daily_Return" not in data.columns:
        raise KeyError("data must contain a 'Daily_Return' column.")

    results = generate_moving_average_signals(
        data, fast_window=fast_window, slow_window=slow_window
    )
    results["Buy_Hold_Return"] = results["Daily_Return"].fillna(0.0)
    results["Strategy_Gross_Return"] = (
        results["Position"] * results["Daily_Return"].fillna(0.0)
    )

    # Count the initial entry as a trade if the strategy starts long.
    position_change = results["Position"].diff().abs()
    if not position_change.empty:
        position_change.iloc[0] = abs(results["Position"].iloc[0])
    results["Position_Change"] = position_change.fillna(0.0)
    results["Transaction_Cost"] = (
        results["Position_Change"] * transaction_cost
    )
    results["Strategy_Net_Return"] = (
        results["Strategy_Gross_Return"] - results["Transaction_Cost"]
    )

    split_index = int(len(results) * train_fraction)
    if split_index <= 0 or split_index >= len(results):
        raise ValueError("Not enough observations for the requested split.")

    train = results.iloc[:split_index].copy()
    test = results.iloc[split_index:].copy()

    # Keep all observations for the full backtest and a separate test slice.
    metrics = {
        "full_strategy": summarize_returns(
            results["Strategy_Net_Return"], risk_free_rate
        ),
        "full_buy_and_hold": summarize_returns(
            results["Buy_Hold_Return"], risk_free_rate
        ),
        "test_strategy": summarize_returns(
            test["Strategy_Net_Return"], risk_free_rate
        ),
        "test_buy_and_hold": summarize_returns(
            test["Buy_Hold_Return"], risk_free_rate
        ),
    }

    return {
        "results": results,
        "train": train,
        "test": test,
        "split_date": test.index[0],
        "metrics": metrics,
    }
