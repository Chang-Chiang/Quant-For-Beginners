# Notebooks 学习入口

## 从这里开始

按顺序打开，先完成 **Phase 1**，再进入 **Phase 2**。

### Phase 1：量化入门（`phase1_intro/`）

| 顺序 | 文件 | 等级 | 核心问题 |
|------|------|------|---------|
| 1 | [01_什么是量化金融.ipynb](phase1_intro/01_什么是量化金融.ipynb) | Lv.1 量化探索者 | 量化交易是什么？ |
| 2 | [02_你的第一个量化实验.ipynb](phase1_intro/02_你的第一个量化实验.ipynb) | Lv.1 数据分析 | 怎么用 Python 看行情？ |
| 3 | [03_移动平均线策略.ipynb](phase1_intro/03_移动平均线策略.ipynb) | Lv.2 策略设计师 | 均线金叉死叉能赚钱吗？ |
| 4 | [04_策略回测.ipynb](phase1_intro/04_策略回测.ipynb) | Lv.3 回测分析师 | 策略真的有效吗？怎么验证？ |

### Phase 2：风险与组合管理（`phase2_intro/`）

| 顺序 | 文件 | 等级 | 核心问题 |
|------|------|------|---------|
| 5 | [01_理解波动率.ipynb](phase2_intro/01_理解波动率.ipynb) | Lv.3 风险感知者 | 收益相同，体验为什么天差地别？ |
| 6 | [02_夏普比率与Beta.ipynb](phase2_intro/02_夏普比率与Beta.ipynb) | Lv.4 风险分析师 | 怎么衡量「性价比」和「跟大盘多紧」？ |
| 7 | [03_最大回撤与仓位管理.ipynb](phase2_intro/03_最大回撤与仓位管理.ipynb) | Lv.5 仓位管理员 | 最惨能亏多少？买多少合适？ |
| 8 | [04_多标的组合与相关性.ipynb](phase2_intro/04_多标的组合与相关性.ipynb) | Lv.5 组合分析师 | 多买几只，真的更稳吗？ |

## 互动演示

部分章节配有 **可交互 HTML 演示**，帮助理解公式背后的直觉：

| 演示 | 关联章节 | 说明 |
|------|---------|------|
| [日收益率计算](../assets/interactive/daily-return-demo.html) | Phase 2 · 第5章 | 逐日代入公式，看 $r_t$ 如何计算 |
| [样本标准差](../assets/interactive/std-dev-demo.html) | Phase 2 · 第5章 | 逐步累加偏差平方，算出 $\sigma$ |
| [总体方差](../assets/interactive/population-variance-demo.html) | Phase 2 · 第5章 | 除以 $N$ 的方差计算过程 |
| [方差公式对比](../assets/interactive/variance-formulas-demo.html) | Phase 2 · 第5章 | ÷$N$ vs ÷$(N{-}1)$、詹森不等式蒙特卡洛 |
| [夏普比率](../assets/interactive/sharpe-ratio-demo.html) | Phase 2 · 第6章 | 代入收益、无风险利率、波动，算出 Sharpe |
| [Beta 计算](../assets/interactive/beta-demo.html) | Phase 2 · 第6章 | 逐步代入 Cov / Var，算出 β |

> 所有演示均在浏览器打开，无需安装 Python。

## 每章结构（统一）

1. **本章你将学会** + 当前等级 + 难度 + 时间
2. 概念讲解（人话，不论文体）
3. 可运行代码 + 可视化
4. **🎯 挑战任务** + 总结

## 编写原则

- 每章只讲一个核心概念
- 每章必须有可运行结果
- 每章至少一张「值得截图」的图

## 后续目录（规划）

- `phase3_intro/` — AI 量化入门（第 9～12 章）

详见根目录 [README.md](../README.md) 与 [docs/ROADMAP.md](../docs/ROADMAP.md)。
