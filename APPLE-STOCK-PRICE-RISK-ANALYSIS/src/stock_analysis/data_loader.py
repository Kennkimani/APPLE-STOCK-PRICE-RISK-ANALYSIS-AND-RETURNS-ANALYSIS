"""Download and prepare historical market data."""

from __future__ import annotations

import pandas as pd


def load_stock_data(
    ticker: str = "AAPL",
    period: str = "5y",
    interval: str = "1d",
) -> pd.DataFrame:
    """Download adjusted historical prices and calculate daily close returns.

    Uses auto-adjusted OHLC prices so dividends and splits are reflected in
    the adjusted price history. The first daily return is NaN by definition.
    """
    # Import inside the function so the metrics/strategy modules can be
    # imported and unit-tested without requiring a network-data client.
    import yfinance as yf

    data = yf.download(
        ticker,
        period=period,
        interval=interval,
        auto_adjust=True,
        progress=False,
    )

    if data.empty:
        raise ValueError(f"No market data returned for ticker {ticker!r}.")

    # yfinance may return MultiIndex columns depending on version/options.
    if isinstance(data.columns, pd.MultiIndex):
        data.columns = data.columns.get_level_values(0)

    data = data.copy()
    data.index = pd.to_datetime(data.index)
    data = data.sort_index()
    data = data[~data.index.duplicated(keep="last")]

    if "Close" not in data.columns:
        raise ValueError("Downloaded data does not contain a 'Close' column.")

    data["Daily_Return"] = data["Close"].pct_change()
    return data
