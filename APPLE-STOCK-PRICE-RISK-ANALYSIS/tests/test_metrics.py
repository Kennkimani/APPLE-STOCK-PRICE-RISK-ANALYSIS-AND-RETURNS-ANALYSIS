import numpy as np
import pandas as pd

from stock_analysis.metrics import (
    calculate_cumulative_returns,
    calculate_max_drawdown,
    calculate_sharpe_ratio,
    calculate_total_return,
)


def test_total_return_compounds_periodic_returns():
    returns = pd.Series([0.10, -0.10])
    assert np.isclose(calculate_total_return(returns), -0.01)


def test_cumulative_returns():
    returns = pd.Series([0.10, -0.10])
    result = calculate_cumulative_returns(returns)
    assert np.isclose(result.iloc[-1], -0.01)


def test_max_drawdown_includes_initial_capital():
    returns = pd.Series([-0.10, 0.05])
    assert np.isclose(calculate_max_drawdown(returns), -0.10)


def test_sharpe_is_nan_for_constant_returns():
    returns = pd.Series([0.01] * 10)
    assert np.isnan(calculate_sharpe_ratio(returns, risk_free_rate=0.0))
