"""
双均线策略模块：信号生成与金叉/死叉检测。
"""

import numpy as np
import pandas as pd


def generate_signal(
    close: pd.Series, short_window: int = 5, long_window: int = 20
) -> pd.Series:
    """生成双均线交易信号。

    MA_short > MA_long → signal = 1（持仓）
    MA_short <= MA_long → signal = 0（空仓）

    Args:
        close: 收盘价序列
        short_window: 短期均线窗口，默认 5
        long_window: 长期均线窗口，默认 20

    Returns:
        信号序列（1=持仓, 0=空仓），前 long_window-1 行为 NaN
    """
    ma_short = close.rolling(short_window).mean()
    ma_long = close.rolling(long_window).mean()
    signal = (ma_short > ma_long).astype(int)
    signal.iloc[: long_window - 1] = np.nan
    return signal


def detect_crossover(short_ma: pd.Series, long_ma: pd.Series) -> pd.Series:
    """检测金叉/死叉。

    返回值：
        +1 = 金叉（短均线从下穿上长均线）
        -1 = 死叉（短均线从上穿下长均线）
         0 = 无交叉

    Args:
        short_ma: 短期均线序列
        long_ma: 长期均线序列

    Returns:
        交叉信号序列
    """
    spread = short_ma - long_ma
    cross = np.sign(spread).diff()
    return cross.fillna(0)
