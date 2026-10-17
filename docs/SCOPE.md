# Scope

## The ask
Identify Indian sectors that have significantly underperformed the market over long horizons, separate structural laggards from short-term noise, and flag which (if any) are near a trend change. Make the analysis rerunnable and the code reviewable.

## In scope
- 17 sector ETFs and 4 NSE price indices available on Yahoo Finance.
- 3/5/10-year CAGR and excess vs Nifty 50; rolling 3-year consistency.
- Drawdown from 52-week high; 200-SMA trend state.

## Out of scope
- Valuation (P/E, P/B) or earnings-cycle analysis.
- Stock selection within a sector.
- Index constituent-level attribution.

## Assumptions
- Sector ETFs approximate their sector index closely enough for multi-year comparison.
- Benchmark is NIFTYBEES (total-return-like) when comparing ETFs, ^NSEI when comparing price indices.

## Success criteria
- Tests pass offline; live run produces a ranked table with an as-of date.
- Short-history sectors return blanks, not wrong numbers.
