"""
收益率计算模块：日收益率、累计收益率、年化指标。
"""

import numpy as np
import pandas as pd

TRADING_DAYS = 252  # 美股年交易日数


def daily_returns(close: pd.Series) -> pd.Series:
    """计算日收益率 r_t = (P_t - P_{t-1}) / P_{t-1}。

    Args:
        close: 收盘价序列

    Returns:
        日收益率序列（第一天为 NaN）
    """
    return close.pct_change()


def cumulative_returns(daily_ret: pd.Series) -> pd.Series:
    """计算累计收益率。

    Args:
        daily_ret: 日收益率序列

    Returns:
        累计收益率序列，起点为 0
    """
    return (1 + daily_ret).cumprod() - 1


def annualize_return(daily_returns: pd.Series) -> float:
    """日收益率 → 年化收益率（复利近似）。

    Args:
        daily_returns: 日收益率序列

    Returns:
        年化收益率
    """
    mean_daily = daily_returns.mean()
    return (1 + mean_daily) ** TRADING_DAYS - 1


def annualize_volatility(daily_returns: pd.Series) -> float:
    """日收益率 → 年化波动率。

    Args:
        daily_returns: 日收益率序列

    Returns:
        年化波动率 = 日标准差 × √252
    """
    daily_std = daily_returns.std()
    return daily_std * np.sqrt(TRADING_DAYS)
