# Methodology

**CAGR.** (last ÷ price on the last session on or before *T − N years*)^(1/N) − 1. If history doesn't reach back N years the value is blank.

**Excess.** Sector CAGR − benchmark CAGR, in percentage points per year.

**Rolling consistency.** Rolling 3-year CAGR (756 sessions) for sector and benchmark on common dates; report the share of windows where the sector won, plus median and latest excess. This separates "always lags" from "one bad stretch".

**Contrarian candidates.** Excess ≤ −2 pp/yr on every available horizon.

**Trend state** (200-day SMA, 22-session slope):
- uptrend: price above a rising SMA
- downtrend: price below a falling SMA
- basing: mixed, the zone where a Stage 1 → 2 transition starts

## Code-review notes that shaped this version
- `period="11y"` is not a valid yfinance period → use `start=`.
- Short histories must yield blanks, not crashes or silently wrong drawdowns.
- Use `group_by="column"` and handle the single-ticker case so the result shape is stable across yfinance versions.

## Known bias
ETF prices include dividends, price indices don't (~1 pp/yr gap). Compare within one family.
