"""数据获取与收益率计算。"""

from src.data.fetcher import fetch_us_close, fetch_us_prices
from src.data.returns import (
    daily_returns,
    cumulative_returns,
    annualize_return,
    annualize_volatility,
    TRADING_DAYS,
)

__all__ = [
    "fetch_us_close",
    "fetch_us_prices",
    "daily_returns",
    "cumulative_returns",
    "annualize_return",
    "annualize_volatility",
    "TRADING_DAYS",
]
