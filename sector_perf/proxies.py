"""Instruments used as sector proxies.

Yahoo does not carry most NSE sectoral indices, so liquid sector ETFs are
used. ETF prices are dividend-inclusive (total-return-like), so they run
roughly 1pt/yr above price indices. Compare like with like.
"""
SECTOR_ETFS = {
    "Nifty50": "NIFTYBEES.NS", "IT": "ITBEES.NS", "Bank": "BANKBEES.NS",
    "Pvt Bank": "PVTBANIETF.NS", "PSU Bank": "PSUBNKBEES.NS", "CPSE": "CPSEETF.NS",
    "Infra": "INFRABEES.NS", "Consumption": "CONSUMBEES.NS", "FMCG": "FMCGIETF.NS",
    "Auto": "AUTOBEES.NS", "Pharma": "PHARMABEES.NS", "Healthcare": "HEALTHIETF.NS",
    "Metal": "METALIETF.NS", "Realty": "MOREALTY.NS", "Oil & Gas": "OILIETF.NS",
    "MNC": "MNC.NS", "Div Opp": "DIVOPPBEES.NS",
}
# Price indices Yahoo does carry: longer history, price-only (no dividends).
SECTOR_INDICES = {
    "Nifty50": "^NSEI", "IT": "^CNXIT", "Bank": "^NSEBANK", "Pharma": "^CNXPHARMA",
}
BENCHMARK = "Nifty50"
