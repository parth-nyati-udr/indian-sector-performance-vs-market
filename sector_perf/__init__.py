"""sector-relative-performance: long-horizon sector laggard / leader analysis for India."""
from .metrics import cagr, rolling_cagr, drawdown_from_high, trend_state
from .analysis import horizon_table, rolling_table, contrarian_candidates
from .proxies import SECTOR_ETFS, SECTOR_INDICES

__version__ = "1.0.0"
