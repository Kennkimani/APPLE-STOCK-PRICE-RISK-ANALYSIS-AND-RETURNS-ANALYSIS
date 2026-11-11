"""Return and risk metric calculations."""

from __future__ import annotations

import numpy as np
import pandas as pd


def calculate_cumulative_returns(returns: pd.Series) -> pd.Series:
    """Convert periodic returns into a cumulative growth series."""
    clean = returns.fillna(0.0)
    return (1.0 + clean).cumprod() - 1.0


def calculate_total_return(returns: pd.Series) -> float:
    """Calculate total compounded return over the supplied period."""
    clean = returns.dropna()
    if clean.empty:
        return float("nan")
    return float((1.0 + clean).prod() - 1.0)


def calculate_annualized_volatility(
    returns: pd.Series, periods_per_year: int = 252
) -> float:
    """Annualize sample standard deviation of periodic returns."""
    clean = returns.dropna()
    if len(clean) < 2:
        return float("nan")
    return float(clean.std(ddof=1) * np.sqrt(periods_per_year))


def calculate_cagr(
    returns: pd.Series, periods_per_year: int = 252
) -> float:
    """Calculate compound annual growth rate from periodic returns."""
    clean = returns.dropna()
    if clean.empty:
        return float("nan")
    years = len(clean) / periods_per_year
    if years <= 0:
        return float("nan")
    growth = float((1.0 + clean).prod())
    if growth < 0:
        return float("nan")
    return float(growth ** (1.0 / years) - 1.0)


def calculate_max_drawdown(returns: pd.Series) -> float:
    """Return the most negative peak-to-trough drawdown.

    The wealth index includes an initial value of 1.0, so an initial loss is
    correctly measured as a drawdown from starting capital.
    """
    clean = returns.fillna(0.0)
    wealth = (1.0 + clean).cumprod()
    wealth_with_initial = pd.concat(
        [pd.Series([1.0], index=[_initial_index(clean)]), wealth]
    )
    running_peak = wealth_with_initial.cummax()
    drawdown = wealth_with_initial / running_peak - 1.0
    return float(drawdown.min()) if not drawdown.empty else float("nan")


def _initial_index(series: pd.Series):
    """Create an index label preceding the first observation where possible."""
    if series.empty:
        return 0
    first = series.index[0]
    if isinstance(first, (pd.Timestamp,)):
        return first - pd.Timedelta(nanoseconds=1)
    return "__initial_capital__"


def calculate_sharpe_ratio(
    returns: pd.Series,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 252,
) -> float:
    """Calculate annualized Sharpe ratio using an effective annual risk-free rate."""
    clean = returns.dropna()
    if len(clean) < 2:
        return float("nan")
    daily_rf = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess_returns = clean - daily_rf
    volatility = clean.std(ddof=1)
    if volatility == 0 or pd.isna(volatility):
        return float("nan")
    return float(
        excess_returns.mean() / volatility * np.sqrt(periods_per_year)
    )


def summarize_returns(
    returns: pd.Series,
    risk_free_rate: float = 0.04,
    periods_per_year: int = 252,
) -> dict[str, float]:
    """Return a consistent set of headline performance metrics."""
    return {
        "total_return": calculate_total_return(returns),
        "cagr": calculate_cagr(returns, periods_per_year),
        "annualized_volatility": calculate_annualized_volatility(
            returns, periods_per_year
        ),
        "max_drawdown": calculate_max_drawdown(returns),
        "sharpe_ratio": calculate_sharpe_ratio(
            returns, risk_free_rate, periods_per_year
        ),
    }
