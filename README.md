# sector-relative-performance

Which Indian sectors have **structurally** lagged or led the market, and are any of them turning? A contrarian-research tool comparing sector proxies against the Nifty 50 over 3, 5 and 10 years, with rolling-window consistency and a trend-state gate.

## Output
| Table | Answers |
|---|---|
| `horizon_table` | CAGR per horizon, excess vs Nifty 50 (pp/yr), drawdown from 52w high, trend state |
| `rolling_table` | In what % of rolling 3-year windows did each sector beat the market? |
| `contrarian_candidates` | Sectors lagging by ≥ 2 pp/yr on **every** horizon |

## Install & run
```bash
pip install -e ".[dev]"
python -c "
from sector_perf import SECTOR_ETFS, horizon_table, contrarian_candidates
from sector_perf.analysis import download
t = horizon_table(download(SECTOR_ETFS), 'Nifty50')
print(t); print(contrarian_candidates(t))"
```

## Layout
```
sector_perf/
  proxies.py   sector ETF and index tickers (with total-return caveat)
  metrics.py   cagr, rolling_cagr, drawdown_from_high, trend_state (pure)
  analysis.py  horizon / rolling / contrarian tables + downloader
tests/         9 offline tests on exact-growth price paths
docs/          SCOPE.md, METHODOLOGY.md, TEST_PLAN.md
```

## Reading the output
A laggard in a `downtrend` is a watchlist name, not a buy. The contrarian entry is when it moves to `basing` and then to `uptrend` (Weinstein Stage 1 → 2).

## Limitations
Sector ETFs are proxies and several have short histories, so 10-year figures may be missing. ETF prices include dividends; price indices do not, so don't mix them in one comparison. Research tool, not investment advice.

## License
MIT
