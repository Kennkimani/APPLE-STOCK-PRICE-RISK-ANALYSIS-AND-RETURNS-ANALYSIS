"""Reusable tools for stock risk, return, and strategy analysis."""

from .data_loader import load_stock_data
from .metrics import (
    calculate_cagr,
    calculate_cumulative_returns,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_total_return,
    calculate_annualized_volatility,
)
from .strategy import generate_moving_average_signals
from .backtester import run_backtest

__all__ = [
    "load_stock_data",
    "calculate_cagr",
    "calculate_cumulative_returns",
    "calculate_max_drawdown",
    "calculate_sharpe_ratio",
    "calculate_total_return",
    "calculate_annualized_volatility",
    "generate_moving_average_signals",
    "run_backtest",
]
