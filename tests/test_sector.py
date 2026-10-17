import numpy as np
import pandas as pd
import pytest

from sector_perf import (cagr, contrarian_candidates, drawdown_from_high,
                         horizon_table, rolling_cagr, rolling_table, trend_state)

IDX = pd.bdate_range("2014-01-01", "2026-10-15")


def growth(rate):
    """Exact compounding path at `rate` per year on business days."""
    t = (IDX - IDX[0]).days / 365.25
    return pd.Series(100 * (1 + rate) ** t, index=IDX)


def test_cagr_recovers_known_rate():
    assert cagr(growth(0.12), 5) == pytest.approx(0.12, abs=0.002)


def test_cagr_none_when_history_short():
    assert cagr(growth(0.1).iloc[-500:], 5) is None


def test_rolling_cagr_constant_for_constant_growth():
    r = rolling_cagr(growth(0.10), 3)
    assert r.between(0.095, 0.105).all()


def test_drawdown():
    s = pd.Series([100.0] * 200 + [120.0] + [90.0] * 60)
    assert drawdown_from_high(s) == pytest.approx(-0.25)
    assert drawdown_from_high(s.iloc[:100]) is None


def test_trend_states():
    assert trend_state(growth(0.15)) == "uptrend"
    assert trend_state(growth(-0.15)) == "downtrend"
    # fresh 12% drop below a still-rising 200 SMA
    pullback = growth(0.2).copy()
    pullback.iloc[-5:] = pullback.iloc[-6] * 0.88
    assert trend_state(pullback) == "basing"


@pytest.fixture
def panel():
    return pd.DataFrame({"Nifty50": growth(0.12), "IT": growth(0.04),
                         "Defence": growth(0.25), "Flat": growth(0.115)})


def test_horizon_table_excess_and_order(panel):
    t = horizon_table(panel, "Nifty50")
    assert t.index[0] == "IT"                       # worst first
    assert t.loc["IT", "5y_vs_bench"] == pytest.approx(-8, abs=0.3)
    assert t.loc["Nifty50", "5y_vs_bench"] == 0


def test_contrarian_requires_all_horizons(panel):
    c = contrarian_candidates(horizon_table(panel, "Nifty50"), max_excess=-2)
    assert list(c.index) == ["IT"]                  # 'Flat' lags only ~0.5pp


def test_rolling_table(panel):
    r = rolling_table(panel, "Nifty50", 3)
    assert r.loc["IT", "beat_bench_%"] == 0 and r.loc["Defence", "beat_bench_%"] == 100


def test_short_history_sector_gets_none(panel):
    panel["New"] = growth(0.3).where(IDX > "2023-06-01")
    t = horizon_table(panel, "Nifty50")
    assert pd.isna(t.loc["New", "5y_%"]) and not pd.isna(t.loc["New", "3y_%"])
