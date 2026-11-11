import pandas as pd

from stock_analysis.strategy import generate_moving_average_signals


def test_position_is_lagged_one_observation():
    index = pd.date_range("2024-01-01", periods=8, freq="D")
    prices = pd.DataFrame({"Close": [10, 9, 8, 9, 10, 11, 12, 13]}, index=index)
    result = generate_moving_average_signals(
        prices, fast_window=2, slow_window=3
    )
    assert result["Position"].iloc[0] == 0
    assert result["Position"].iloc[1] == result["Signal"].iloc[0]


def test_fast_window_must_be_less_than_slow_window():
    prices = pd.DataFrame({"Close": [1, 2, 3]})
    try:
        generate_moving_average_signals(prices, fast_window=3, slow_window=2)
    except ValueError:
        pass
    else:
        raise AssertionError("Expected ValueError")
