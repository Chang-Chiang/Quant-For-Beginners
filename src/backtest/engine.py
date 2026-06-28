"""
回测引擎：模拟交易并计算策略净值。
"""

import pandas as pd
import numpy as np


def run_backtest(close: pd.Series, signal: pd.Series) -> pd.DataFrame:
    """运行回测：将信号转化为仓位、策略收益和净值曲线。

    信号推迟一天执行（避免未来函数）：今天收盘算出的信号，明天才能按它交易。

    Args:
        close: 收盘价序列
        signal: 交易信号序列（1=持仓, 0=空仓）

    Returns:
        DataFrame 包含以下列：
        - close: 收盘价
        - ret: 日收益率
        - signal: 原始信号
        - position: 实际仓位（shift(1)）
        - strategy_ret: 策略日收益
        - nav: 策略净值
        - buyhold_ret: 买入持有日收益
        - nav_buyhold: 买入持有净值
    """
    df = pd.DataFrame({"close": close})
    df["ret"] = df["close"].pct_change().fillna(0)
    df["signal"] = signal
    df["position"] = df["signal"].shift(1).fillna(0).astype(int)
    df["strategy_ret"] = df["position"] * df["ret"]
    df["nav"] = (1 + df["strategy_ret"]).cumprod()
    df["buyhold_ret"] = df["ret"]
    df["nav_buyhold"] = (1 + df["buyhold_ret"]).cumprod()
    return df


def buy_hold_equity(daily_returns: pd.Series) -> pd.Series:
    """买入持有净值曲线。

    Args:
        daily_returns: 日收益率序列

    Returns:
        净值曲线，起点 ≈ 1
    """
    return (1 + daily_returns).cumprod()


def compute_win_rate(trades_df: pd.DataFrame) -> dict:
    """统计交易胜率。

    Args:
        trades_df: 包含 'action', 'close' 列的 DataFrame，
                   action 为 '买入' 或 '卖出'

    Returns:
        dict 包含 total_rounds, wins, losses, win_rate
    """
    wins, losses = 0, 0
    entry_price = None

    for _, row in trades_df.iterrows():
        if row["action"] == "买入":
            entry_price = row["close"]
        elif row["action"] == "卖出" and entry_price is not None:
            pnl = row["close"] / entry_price - 1
            if pnl > 0:
                wins += 1
            else:
                losses += 1
            entry_price = None

    total = wins + losses
    return {
        "total_rounds": total,
        "wins": wins,
        "losses": losses,
        "win_rate": wins / total if total > 0 else np.nan,
    }
