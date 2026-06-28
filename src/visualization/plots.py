"""
可视化模块：净值曲线、水下曲线、热力图、风险收益散点图。
"""

from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter


def setup_chinese_font():
    """配置 matplotlib 中文字体，兼容 Windows / Mac / Linux。"""
    import matplotlib.font_manager as fm

    cn_fonts = [
        "SimHei",
        "PingFang SC",
        "Noto Sans CJK SC",
        "WenQuanYi Micro Hei",
        "Droid Sans Fallback",
    ]
    available = {f.name for f in fm.fontManager.ttflist}
    for font in cn_fonts:
        if font in available:
            plt.rcParams["font.sans-serif"] = [font]
            break
    else:
        plt.rcParams["font.sans-serif"] = [cn_fonts[-1]]
    plt.rcParams["axes.unicode_minus"] = False


def _finalize(fig, save_path: str | None = None):
    """统一处理图表结尾：保存或显示。"""
    plt.tight_layout()
    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        fig.savefig(save_path, dpi=150, bbox_inches="tight")
        plt.close(fig)
        print(f"📊 图表已保存: {save_path}")
    else:
        plt.show()


def plot_nav_curves(
    nav_dict: dict[str, pd.Series],
    title: str = "净值曲线对比",
    save_path: str | None = None,
):
    """绘制多条净值曲线对比图。

    Args:
        nav_dict: {曲线名称: 净值序列} 字典
        title: 图表标题
        save_path: 保存路径（如 'output/nav.png'），为 None 则弹窗显示
    """
    fig, ax = plt.subplots(figsize=(14, 6))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FFFFFF")

    for label, nav in nav_dict.items():
        ax.plot(nav.index, nav, linewidth=1.8, label=label)

    ax.axhline(1.0, color="black", linewidth=0.6, linestyle=":", alpha=0.5)
    ax.set_title(title, fontsize=14)
    ax.set_xlabel("日期")
    ax.set_ylabel("净值（起点=1）")
    ax.legend(loc="upper left")
    ax.grid(True, linestyle="--", alpha=0.35)
    _finalize(fig, save_path)


def plot_drawdown(
    equity: pd.Series,
    title: str = "水下曲线",
    save_path: str | None = None,
):
    """绘制水下曲线（回撤填充图）。

    Args:
        equity: 净值曲线
        title: 图表标题
        save_path: 保存路径，为 None 则弹窗显示
    """
    from src.backtest.metrics import compute_drawdown, max_drawdown

    dd = compute_drawdown(equity)
    mdd = max_drawdown(equity)
    running_peak = equity.cummax()

    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(12, 7), sharex=True, gridspec_kw={"height_ratios": [2, 1]}
    )
    fig.patch.set_facecolor("#FAFAFA")

    ax1.set_facecolor("#FFFFFF")
    ax1.plot(equity.index, equity, color="#007AFF", linewidth=1.6, label="净值")
    ax1.plot(
        running_peak.index,
        running_peak,
        color="gray",
        linestyle="--",
        alpha=0.55,
        label="历史最高",
    )
    ax1.set_title(title, fontsize=14)
    ax1.set_ylabel("净值")
    ax1.legend(loc="upper left")
    ax1.grid(True, linestyle="--", alpha=0.35)

    ax2.set_facecolor("#FFFFFF")
    ax2.fill_between(dd.index, dd, 0, color="#E82127", alpha=0.45)
    ax2.axhline(
        mdd, color="#333333", linestyle=":", linewidth=1.2, label=f"最大回撤 {mdd:.1%}"
    )
    ax2.set_ylabel("回撤")
    ax2.set_xlabel("日期")
    ax2.legend(loc="lower left")
    ax2.grid(True, linestyle="--", alpha=0.35)

    _finalize(fig, save_path)


def plot_heatmap(
    corr: pd.DataFrame,
    title: str = "相关性热力图",
    save_path: str | None = None,
):
    """绘制相关性热力图。

    Args:
        corr: 相关系数矩阵
        title: 图表标题
        save_path: 保存路径，为 None 则弹窗显示
    """
    labels = list(corr.columns)
    n = len(labels)

    fig, ax = plt.subplots(figsize=(8.5, 6.5))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FFFFFF")

    im = ax.imshow(corr.values, cmap="RdBu_r", vmin=-1, vmax=1)

    ax.set_xticks(range(n))
    ax.set_yticks(range(n))
    ax.set_xticklabels(labels)
    ax.set_yticklabels(labels)
    plt.setp(ax.get_xticklabels(), rotation=45, ha="right")

    for i in range(n):
        for j in range(n):
            rho = corr.iloc[i, j]
            text_color = "white" if abs(rho) > 0.55 else "black"
            ax.text(
                j,
                i,
                f"{rho:.2f}",
                ha="center",
                va="center",
                color=text_color,
                fontsize=10,
                fontweight="bold",
            )

    ax.set_title(title, fontsize=14, pad=12)
    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    _finalize(fig, save_path)


def plot_risk_return_scatter(
    metrics_df: pd.DataFrame,
    title: str = "风险-收益散点图",
    save_path: str | None = None,
):
    """绘制风险收益散点图。

    Args:
        metrics_df: 包含 '年化波动' 和 '年化收益' 列的 DataFrame，索引为股票代码
        title: 图表标题
        save_path: 保存路径，为 None 则弹窗显示
    """
    fig, ax = plt.subplots(figsize=(10, 7))
    fig.patch.set_facecolor("#FAFAFA")
    ax.set_facecolor("#FFFFFF")

    pct = FuncFormatter(lambda x, _pos: f"{x:.0%}")

    for ticker, row in metrics_df.iterrows():
        vol = row["年化波动"]
        ret = row["年化收益"]
        ax.scatter(vol, ret, s=140, edgecolors="white", linewidths=1.0, zorder=3)
        ax.annotate(
            ticker,
            (vol, ret),
            textcoords="offset points",
            xytext=(6, 5),
            fontsize=9,
            fontweight="bold",
        )

    ax.xaxis.set_major_formatter(pct)
    ax.yaxis.set_major_formatter(pct)
    ax.set_xlabel("年化波动率", fontsize=12)
    ax.set_ylabel("年化收益率", fontsize=12)
    ax.set_title(title, fontsize=14, pad=12)
    ax.grid(True, linestyle="--", alpha=0.35)
    _finalize(fig, save_path)
