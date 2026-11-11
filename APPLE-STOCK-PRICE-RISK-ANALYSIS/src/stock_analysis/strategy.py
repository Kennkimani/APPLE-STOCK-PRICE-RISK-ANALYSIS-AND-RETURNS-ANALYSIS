"""Moving-average crossover signal generation."""

from __future__ import annotations

import pandas as pd


def generate_moving_average_signals(
    data: pd.DataFrame,
    fast_window: int = 20,
    slow_window: int = 50,
    price_column: str = "Close",
) -> pd.DataFrame:
    """Add moving averages, signals, and executable positions to price data.

    A long signal is generated when the fast moving average is above the slow
    moving average. The position is shifted by one observation so a signal
    calculated from today's close cannot earn today's close-to-close return.
    """
    if fast_window <= 0 or slow_window <= 0:
        raise ValueError("Moving-average windows must be positive integers.")
    if fast_window >= slow_window:
        raise ValueError("fast_window must be smaller than slow_window.")
    if price_column not in data.columns:
        raise KeyError(f"Missing price column: {price_column}")

    result = data.copy()
    result["Fast_MA"] = result[price_column].rolling(
        window=fast_window, min_periods=fast_window
    ).mean()
    result["Slow_MA"] = result[price_column].rolling(
        window=slow_window, min_periods=slow_window
    ).mean()

    result["Signal"] = (
        result["Fast_MA"] > result["Slow_MA"]
    ).astype(int)
    result.loc[result["Slow_MA"].isna(), "Signal"] = 0

    # Position used for a day's return comes from the previous day's close.
    result["Position"] = result["Signal"].shift(1).fillna(0).astype(int)
    return result
