# src/matplot/line_plot.py
from typing import Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from config import settings
from config.visualization_config import MATPLOT_LINE_CONFIG
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False

def create_line_plot(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        time_col: str = "timestamp",
        value_col: str = "temperature",
        show: bool = False,
        **kwargs) -> None:
    """
    重构后的参数集中式折线图

    参数：
    df : 必须传入的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名称（覆盖config）
    value_col : 数值列名称（覆盖config）
    show : 是否显示图表（强制参数）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_LINE_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    line_params = final_config["line"]
    axis_params = final_config["axis"]
    text_params = final_config["text"]
    legend_params = final_config["legend"]
    output_params = final_config["output"]

    # 创建画布
    plt.figure(
        figsize=fig_params["figsize"],
        dpi=fig_params["dpi"]
    )
    ax = plt.gca()

    # 处理数据
    dates = pd.to_datetime(df[time_col])
    values = df[value_col]

    # 绘制折线
    line = ax.plot(
        dates,
        values,
        color=line_params["color"],
        linestyle = line_params.get("linestyle", "-"),
        linewidth=line_params["linewidth"],
        marker=line_params["marker"],
        markersize=line_params["markersize"],
        alpha=line_params.get("alpha", 0.8),
        label=legend_params["label"]
    )

    # 坐标轴设置
    ax.set_xlabel(axis_params["xlabel"], fontsize=text_params["label_fontsize"])
    ax.set_ylabel(axis_params["ylabel"], fontsize=text_params["label_fontsize"])
    ax.set_title(text_params["title"], fontsize=text_params["title_fontsize"], pad=20)

    # 日期格式化
    locator = mdates.AutoDateLocator()
    formatter = mdates.DateFormatter(axis_params["date_format"])
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # 刻度设置
    plt.xticks(rotation=axis_params["rotation"], ha='right')
    ax.tick_params(axis='both', labelsize=text_params["tick_fontsize"])

    # 网格设置
    if axis_params.get("grid", False):
        ax.grid(
            visible=True,
            linestyle=axis_params["grid_style"]["linestyle"],
            alpha=axis_params["grid_style"]["alpha"]
        )

    # 图例设置
    if legend_params["show"]:
        ax.legend(
            loc=legend_params["loc"],
            fontsize=legend_params.get("fontsize", 12)
        )

    # 保存输出
    if output_params["save_path"]:
        plt.savefig(
            f"{output_params['save_path']}/{output_params['filename']}.png",
            bbox_inches='tight',
            dpi=output_params.get("save_dpi", 300)
        )

    # 显示控制
    if show:
        plt.show()
    plt.close()


def _update_nested_dict(original: dict, updates: dict) -> dict:
    """递归更新嵌套字典"""
    for key, value in updates.items():
        if isinstance(value, dict) and key in original:
            original[key] = _update_nested_dict(original[key], value)
        else:
            original[key] = value
    return original
