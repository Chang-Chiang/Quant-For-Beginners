# 量化学习

基于 [Quant-for-Beginners](https://github.com/yibohere/Quant-for-Beginners) 教程学习后，将 Notebook 中的可复用代码重构为独立 Python 模块。

## 目录

- [项目结构](#项目结构)
- [快速开始](#快速开始)
- [模块说明](#模块说明)
- [教程笔记](#教程笔记)
- [参考](#参考)

---

## 项目结构

```
├── src/                       # 重构后的 Python 模块
│   ├── data/                  # 数据获取与收益率计算
│   ├── strategies/            # 策略逻辑（双均线信号生成）
│   ├── backtest/              # 回测引擎与风险指标
│   ├── portfolio/             # 组合分析（等权组合、相关性）
│   ├── visualization/         # 可视化（净值曲线、热力图等）
│   └── main.py                # 示例入口
├── notebooks/                 # 原始教程 Notebook
│   ├── phase1_intro/          # Phase 1：量化入门（4 章）
│   └── phase2_intro/          # Phase 2：风险与组合管理（4 章）
├── assets/interactive/        # 交互式 HTML 演示
├── docs/
│   ├── notes.md               # 学习笔记
│   └── ROADMAP.md             # 原项目路线图
└── requirements.txt
```

---

## 快速开始

```bash
pip install -r requirements.txt
python src/main.py
```

`main.py` 演示完整流程：下载 AAPL 数据 → 双均线策略回测 → 输出指标 → 保存图表到 `output/`。

---

## 模块说明

### data — 数据获取与收益率

```python
from src.data import fetch_us_close, daily_returns, annualize_volatility

close = fetch_us_close("AAPL", years=2)
ret = daily_returns(close).dropna()
vol = annualize_volatility(ret)
```

- `fetch_us_close(symbol, years)` — AkShare 下载美股收盘价
- `fetch_us_prices(tickers, years)` — 批量下载，返回对齐宽表
- `daily_returns(close)` — 日收益率 `pct_change()`
- `annualize_return / annualize_volatility` — 年化指标

### strategies — 策略逻辑

```python
from src.strategies import generate_signal, detect_crossover

signal = generate_signal(close, short_window=5, long_window=20)
```

- `generate_signal(close, short, long)` — 双均线信号（1=持仓, 0=空仓）
- `detect_crossover(short_ma, long_ma)` — 金叉/死叉检测

### backtest — 回测与风险指标

```python
from src.backtest import run_backtest, max_drawdown, sharpe_ratio, beta_vs_market

result = run_backtest(close, signal)
print(max_drawdown(result["nav"]))
print(sharpe_ratio(ret))
```

- `run_backtest(close, signal)` — 模拟交易，返回含净值的 DataFrame
- `max_drawdown(equity)` / `compute_drawdown(equity)` — 最大回撤
- `sharpe_ratio(ret, rf)` — 夏普比率
- `beta_vs_market(stock, market)` — Beta

### portfolio — 组合分析

```python
from src.portfolio import equal_weight_returns, correlation_matrix

port_ret = equal_weight_returns(returns, ["AAPL", "MSFT", "JPM", "XLE"])
corr = correlation_matrix(returns)
```

### visualization — 可视化

```python
from src.visualization import plot_nav_curves, plot_drawdown, plot_heatmap

plot_nav_curves({"策略": nav, "买入持有": bh}, save_path="output/nav.png")
```

所有画图函数支持 `save_path` 参数：传路径则保存文件，为 `None` 则弹窗显示。

---

## 教程笔记

学习过程中的要点整理见 [docs/notes.md](docs/notes.md)，覆盖 8 章核心概念、公式和代码模式。

原始 Notebook 课程目录见 [notebooks/README.md](notebooks/README.md)。

---

## 参考

- 原教程： [Quant-for-Beginners](https://github.com/yibohere/Quant-for-Beginners) by [Yibo Cheng (@yibohere)](https://github.com/yibohere)

---

## 免责声明

本仓库仅供学习与研究，**不构成任何投资建议**。历史回测结果不代表未来表现，市场有风险。
