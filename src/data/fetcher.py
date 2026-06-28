"""
数据获取模块：从 AkShare 下载美股日线行情。

数据源：AkShare → 新浪财经 → 美股前复权日线
"""

import pandas as pd
import akshare as ak


def fetch_us_close(symbol: str, years: float = 3.0) -> pd.Series:
    """下载单只美股前复权收盘价。

    Args:
        symbol: 股票代码，如 'AAPL', 'TSLA'
        years: 回溯年数，默认 3 年

    Returns:
        以日期为索引的收盘价 Series，名称为 symbol
    """
    start = (
        pd.Timestamp.today() - pd.DateOffset(years=years, days=30)
    ).strftime("%Y-%m-%d")

    df = ak.stock_us_daily(symbol=symbol, adjust="qfq")
    if df is None or df.empty:
        raise RuntimeError(f"{symbol} 未返回数据，请检查网络或 akshare 版本")

    df["date"] = pd.to_datetime(df["date"])
    close = (
        df.set_index("date")
        .sort_index()["close"]
        .loc[lambda s: s.index >= start]
        .rename(symbol)
    )
    return close


def fetch_us_prices(tickers: list[str], years: float = 3.0) -> pd.DataFrame:
    """批量下载多只美股收盘价，返回宽表（列=标的，行=日期）。

    Args:
        tickers: 股票代码列表
        years: 回溯年数

    Returns:
        对齐后的收盘价宽表，已删除缺失行
    """
    frames = {t: fetch_us_close(t, years) for t in tickers}
    return pd.DataFrame(frames).dropna()
