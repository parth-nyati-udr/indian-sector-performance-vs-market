"""Cross-sectional tables built from the metric functions."""
from __future__ import annotations

import pandas as pd

from .metrics import cagr, drawdown_from_high, rolling_cagr, trend_state

HORIZONS = (3, 5, 10)


def horizon_table(prices: pd.DataFrame, benchmark: str, horizons=HORIZONS) -> pd.DataFrame:
    """CAGR per horizon, excess vs benchmark (pp/yr), drawdown and trend state.

    prices: DataFrame, one column per sector label (must include `benchmark`).
    Sorted by 5y excess, worst first.
    """
    rows = {}
    for name in prices.columns:
        s = prices[name].dropna()
        if s.empty:
            continue
        row = {"since": s.index[0].date()}
        for y in horizons:
            v = cagr(s, y)
            row[f"{y}y_%"] = None if v is None else round(v * 100, 1)
        dd = drawdown_from_high(s)
        row["off_52w_hi_%"] = None if dd is None else round(dd * 100, 1)
        row["trend"] = trend_state(s)
        rows[name] = row
    df = pd.DataFrame(rows).T
    for y in horizons:
        col = f"{y}y_%"
        df[col] = pd.to_numeric(df[col])
        df[f"{y}y_vs_bench"] = (df[col] - df.loc[benchmark, col]).round(1)
    sort_col = f"{horizons[1]}y_vs_bench" if len(horizons) > 1 else f"{horizons[0]}y_vs_bench"
    return df.sort_values(sort_col, na_position="last")


def rolling_table(prices: pd.DataFrame, benchmark: str, years: int = 3) -> pd.DataFrame:
    """Share of rolling windows in which each sector beat the benchmark.

    A sector that lagged in 90% of 3-year windows is structurally weak; one
    that lagged in 40% just had a bad recent stretch.
    """
    bench = rolling_cagr(prices[benchmark], years)
    out = {}
    for name in prices.columns:
        if name == benchmark:
            continue
        r = rolling_cagr(prices[name], years)
        both = pd.concat([r, bench], axis=1, join="inner").dropna()
        if both.empty:
            continue
        excess = both.iloc[:, 0] - both.iloc[:, 1]
        out[name] = {"windows": len(excess),
                     "beat_bench_%": round((excess > 0).mean() * 100, 0),
                     "median_excess_pp": round(excess.median() * 100, 1),
                     "latest_excess_pp": round(excess.iloc[-1] * 100, 1)}
    return pd.DataFrame(out).T.sort_values("beat_bench_%")


def contrarian_candidates(table: pd.DataFrame, max_excess: float = -2.0) -> pd.DataFrame:
    """Sectors lagging the benchmark by >= |max_excess| pp/yr on EVERY available
    horizon. Long-duration laggards, not one-period noise.

    Trend state is kept in the output on purpose: a laggard still in a
    downtrend is a watchlist name, not a buy.
    """
    cols = [c for c in table.columns if c.endswith("_vs_bench")]
    lag = table[cols].apply(lambda r: r.dropna().le(max_excess).all() and r.notna().any(), axis=1)
    return table[lag]


def download(tickers: dict[str, str], start: str = "2014-01-01") -> pd.DataFrame:
    """Close prices as one DataFrame with sector labels as columns. Needs network."""
    import yfinance as yf
    px = yf.download(list(tickers.values()), start=start, auto_adjust=True,
                     progress=False, group_by="column")["Close"]
    if isinstance(px, pd.Series):  # single ticker
        px = px.to_frame(next(iter(tickers.values())))
    px.columns.name = None
    inverse = {v: k for k, v in tickers.items()}
    return px.rename(columns=inverse)[[k for k, v in tickers.items() if v in px.columns]]
