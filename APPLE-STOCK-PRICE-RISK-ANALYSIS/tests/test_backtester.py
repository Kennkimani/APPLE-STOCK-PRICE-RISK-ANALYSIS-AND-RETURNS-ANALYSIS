import numpy as np
import pandas as pd

from stock_analysis.backtester import run_backtest


def test_backtest_has_chronological_split_and_costs():
    index = pd.date_range("2020-01-01", periods=120, freq="B")
    close = pd.Series(np.linspace(100, 150, len(index)), index=index)
    data = pd.DataFrame({"Close": close})
    data["Daily_Return"] = data["Close"].pct_change()

    output = run_backtest(
        data,
        fast_window=5,
        slow_window=15,
        transaction_cost=0.001,
        train_fraction=0.7,
    )

    assert len(output["train"]) + len(output["test"]) == len(data)
    assert output["train"].index.max() < output["test"].index.min()
    assert (output["results"]["Transaction_Cost"] >= 0).all()
