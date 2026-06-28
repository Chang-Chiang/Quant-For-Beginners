# src 目录说明

用于放置可复用的 Python 代码，避免所有逻辑都堆在 Notebook 里。

## 模块结构

```
src/
├── data/              # 数据获取与收益率计算
│   ├── fetcher.py     # fetch_us_close, fetch_us_prices（AkShare 美股行情）
│   └── returns.py     # daily_returns, annualize_return, annualize_volatility
├── strategies/        # 策略逻辑
│   └── ma_crossover.py  # 双均线信号生成、金叉/死叉检测
├── backtest/          # 回测与评估
│   ├── engine.py      # run_backtest, buy_hold_equity, compute_win_rate
│   └── metrics.py     # max_drawdown, sharpe_ratio, beta_vs_market
├── portfolio/         # 组合分析
│   └── analysis.py    # equal_weight_returns, correlation_matrix
├── visualization/     # 可视化
│   └── plots.py       # plot_nav_curves, plot_drawdown, plot_heatmap
└── main.py            # 示例入口（演示完整分析流程）
```

## 快速使用

```python
from src.data import fetch_us_close, daily_returns, annualize_volatility
from src.strategies import generate_signal
from src.backtest import run_backtest, max_drawdown, sharpe_ratio

close = fetch_us_close("AAPL", years=2)
signal = generate_signal(close, short_window=5, long_window=20)
result = run_backtest(close, signal)
print(f"最大回撤: {max_drawdown(result['nav']):.2%}")
```

## 运行示例

```bash
python src/main.py
```
