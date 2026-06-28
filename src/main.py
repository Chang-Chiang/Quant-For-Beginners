"""
示例入口：演示如何用 src 模块完成一次完整分析。

用法：python src/main.py（需联网下载行情数据）
"""

import sys
from pathlib import Path

# 将项目根目录加入 Python 路径，确保 src 包可被导入
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import warnings

warnings.filterwarnings("ignore")

from src.data import fetch_us_close, daily_returns, annualize_return, annualize_volatility
from src.strategies import generate_signal
from src.backtest import run_backtest, max_drawdown, sharpe_ratio
from src.visualization import setup_chinese_font, plot_nav_curves, plot_drawdown

# ── 1. 配置 ──
TICKER = "AAPL"
YEARS = 2
SHORT_WINDOW = 5
LONG_WINDOW = 20

# ── 2. 中文字体 ──
setup_chinese_font()

# ── 3. 下载数据 ──
print(f"正在下载 {TICKER} 近 {YEARS} 年行情...")
close = fetch_us_close(TICKER, years=YEARS)
print(f"共 {len(close)} 个交易日，区间 {close.index[0].date()} → {close.index[-1].date()}")

# ── 4. 收益率分析 ──
ret = daily_returns(close).dropna()
ann_ret = annualize_return(ret)
ann_vol = annualize_volatility(ret)
print(f"\n年化收益: {ann_ret:+.2%}")
print(f"年化波动: {ann_vol:.2%}")

# ── 5. 双均线策略回测 ──
signal = generate_signal(close, SHORT_WINDOW, LONG_WINDOW)
result = run_backtest(close, signal)

mdd = max_drawdown(result["nav"])
sr = sharpe_ratio(ret)

print(f"\n双均线策略 ({SHORT_WINDOW}/{LONG_WINDOW}):")
print(f"  累计收益: {result['nav'].iloc[-1] - 1:+.2%}")
print(f"  最大回撤: {mdd:.2%}")
print(f"  夏普比率: {sr:.2f}")

# ── 6. 可视化（保存到 output/ 目录）──
OUTPUT_DIR = Path(__file__).resolve().parent.parent / "output"

plot_nav_curves(
    {
        f"双均线策略 ({SHORT_WINDOW}/{LONG_WINDOW})": result["nav"],
        "买入持有": result["nav_buyhold"],
    },
    title=f"{TICKER} 策略净值对比",
    save_path=str(OUTPUT_DIR / "nav_curves.png"),
)

plot_drawdown(
    result["nav"],
    title=f"{TICKER} 水下曲线",
    save_path=str(OUTPUT_DIR / "drawdown.png"),
)

print("\n✅ 分析完成")
