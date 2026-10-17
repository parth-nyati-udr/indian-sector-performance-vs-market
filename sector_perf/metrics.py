"""Pure metric functions on a single price series (date-indexed)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def cagr(prices: pd.Series, years: float) -> float | None:
    """Compound annual growth over the trailing `years`.

    Uses the last close on or before (last date - years). Returns None if
    history is shorter than the horizon, rather than a misleading number.
    """
    s = prices.dropna()
    start_cut = s.index[-1] - pd.DateOffset(years=years)
    past = s[s.index <= start_cut]
    if past.empty:
        return None
    return float((s.iloc[-1] / past.iloc[-1]) ** (1 / years) - 1)


def rolling_cagr(prices: pd.Series, years: int) -> pd.Series:
    """CAGR for every window of `years` (~252 sessions/yr), indexed by window end.

    Shows whether underperformance is persistent or one bad stretch.
    """
    s = prices.dropna()
    n = int(252 * years)
    return ((s / s.shift(n)) ** (1 / years) - 1).dropna()


def drawdown_from_high(prices: pd.Series, window: int = 252) -> float | None:
    """Distance below the trailing `window`-session high. None if history too short."""
    s = prices.dropna()
    if len(s) < window:
        return None
    return float(s.iloc[-1] / s.iloc[-window:].max() - 1)


def trend_state(prices: pd.Series, slope_days: int = 22) -> str:
    """Coarse Weinstein-style state from the 200-day SMA.

    'uptrend'   price above a rising 200 SMA
    'downtrend' price below a falling 200 SMA
    'basing'    anything else (the zone contrarians wait for)
    """
    s = prices.dropna()
    ma = s.rolling(200, min_periods=200).mean().dropna()
    if len(ma) <= slope_days:
        return "insufficient"
    rising = ma.iloc[-1] > ma.iloc[-1 - slope_days]
    above = s.iloc[-1] > ma.iloc[-1]
    if above and rising:
        return "uptrend"
    if not above and not rising:
        return "downtrend"
    return "basing"
