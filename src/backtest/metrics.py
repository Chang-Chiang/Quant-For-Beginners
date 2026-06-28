"""
风险指标模块：最大回撤、夏普比率、Beta。
"""

import numpy as np
import pandas as pd

from src.data.returns import annualize_return, annualize_volatility, TRADING_DAYS


def compute_drawdown(equity: pd.Series) -> pd.Series:
    """计算逐日回撤序列。

    回撤 = 当前净值 / 历史最高净值 − 1（值 <= 0）

    Args:
        equity: 净值曲线

    Returns:
        回撤序列（所有值 <= 0）
    """
    running_peak = equity.cummax()
    return equity / running_peak - 1


def max_drawdown(equity: pd.Series) -> float:
    """计算最大回撤。

    Args:
        equity: 净值曲线

    Returns:
        最大回撤（负数，绝对值越大越惨）
    """
    return compute_drawdown(equity).min()


def sharpe_ratio(daily_returns: pd.Series, rf_annual: float = 0.04) -> float:
    """计算夏普比率。

    Sharpe = (年化收益 − 无风险利率) / 年化波动率

    Args:
        daily_returns: 日收益率序列
        rf_annual: 年化无风险利率，默认 4%

    Returns:
        夏普比率
    """
    ann_ret = annualize_return(daily_returns)
    ann_vol = annualize_volatility(daily_returns)
    return (ann_ret - rf_annual) / ann_vol


def beta_vs_market(stock: pd.Series, market: pd.Series) -> float:
    """计算股票相对大盘的 Beta。

    Beta = Cov(R_stock, R_market) / Var(R_market)

    Args:
        stock: 股票日收益率序列
        market: 大盘日收益率序列

    Returns:
        Beta 值
    """
    return stock.cov(market) / market.var()
