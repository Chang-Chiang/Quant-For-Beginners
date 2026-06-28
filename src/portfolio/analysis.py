"""
组合分析模块：等权组合、相关性矩阵。
"""

import pandas as pd


def equal_weight_returns(returns: pd.DataFrame, tickers: list[str]) -> pd.Series:
    """计算等权组合日收益。

    Args:
        returns: 多标的日收益率宽表
        tickers: 组合成分代码列表

    Returns:
        等权组合日收益序列
    """
    return returns[tickers].mean(axis=1)


def correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """计算 Pearson 相关系数矩阵。

    Args:
        returns: 多标的日收益率宽表

    Returns:
        相关系数矩阵
    """
    return returns.corr()
