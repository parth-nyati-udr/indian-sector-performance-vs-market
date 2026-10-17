# Test plan

Run `pytest -q`. All tests use exact compounding paths, so expected values are known analytically.

| Test | Scenario | Expected |
|---|---|---|
| `test_cagr_recovers_known_rate` | 12%/yr path | 5y CAGR ≈ 12% |
| `test_cagr_none_when_history_short` | 2 years of data | 5y CAGR = None |
| `test_rolling_cagr_constant_for_constant_growth` | 10%/yr path | Every window ≈ 10% |
| `test_drawdown` | Peak 120, now 90 | −25%; None if < 252 bars |
| `test_trend_states` | Up / down / fresh pullback | uptrend / downtrend / basing |
| `test_horizon_table_excess_and_order` | 4%, 12%, 25% paths | Worst first; IT ≈ −8 pp |
| `test_contrarian_requires_all_horizons` | Big vs tiny laggard | Only the big laggard |
| `test_rolling_table` | Always-loser vs always-winner | 0% vs 100% |
| `test_short_history_sector_gets_none` | 3-year-old sector | 3y filled, 5y blank |

## Manual checks
Live run prints as-of date; IT/FMCG-type laggards should show their trend state alongside.
