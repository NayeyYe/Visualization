# src/matplot/box_plot.py
from typing import Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import calendar
from config.visualization_config import MATPLOT_BOX_CONFIG
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


def create_box_plot(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        time_col: str = "timestamp",
        value_col: str = "temperature",
        group_by: str = "month",  # 分组方式：month/day/hour
        show: bool = False,
        **kwargs) -> None:
    """
    创建气温箱线图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名称（默认'timestamp'）
    value_col : 数值列名称（默认'temperature'）
    group_by : 数据分组方式（month/day/hour）
    show : 是否显示图表（默认False）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_BOX_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    box_params = final_config["box"]
    axis_params = final_config["axis"]
    text_params = final_config["text"]
    output_params = final_config["output"]

    # 创建画布
    plt.figure(
        figsize=fig_params["figsize"],
        dpi=fig_params["dpi"]
    )
    ax = plt.gca()

    # 数据处理
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])

    # 根据分组方式创建分组标签
    if group_by == "month":
        df["group"] = df[time_col].dt.month
        labels = [calendar.month_abbr[i] for i in range(1, 13)]
        xlabel = "月份"
    elif group_by == "day":
        df["group"] = df[time_col].dt.day
        labels = list(range(1, 32))
        xlabel = "日期"
    elif group_by == "hour":
        df["group"] = df[time_col].dt.hour
        labels = [f"{i:02d}:00" for i in range(24)]
        xlabel = "小时"
    else:
        raise ValueError("group_by参数必须是month/day/hour")

    # 准备箱线图数据
    grouped = df.groupby("group")[value_col].apply(list)
    data = [grouped[i] for i in sorted(grouped.index)]

    # 绘制箱线图
    box = ax.boxplot(
        data,
        patch_artist=box_params.get("patch_artist", True),
        showmeans=box_params.get("show_means", True),
        showfliers=box_params.get("show_fliers", True),
        widths=box_params["widths"]
    )

    # 样式设置
    if box_params.get("patch_artist", True):
        for patch in box['boxes']:
            patch.set_facecolor(box_params["facecolor"])
            patch.set_alpha(box_params.get("alpha",0.8))

    for element in ['whiskers', 'caps', 'medians']:
        plt.setp(box[element], color=box_params.get("edgecolor", "#2c3e50"), linewidth=box_params.get("linewidth", 1.5))

    for flier in box['fliers']:
        flier.set(marker=box_params.get("flier_marker", "o"),
                  markersize=box_params.get("flier_size", 4),
                  markerfacecolor=box_params["flier_color"],
                  alpha=box_params.get("flier_alpha", 0.5))

    # 坐标轴设置
    ax.set_xlabel(axis_params["xlabel"] or xlabel, fontsize=text_params.get("label_fontsize", 14))
    ax.set_ylabel(axis_params["ylabel"], fontsize=text_params.get("label_fontsize", 14))
    ax.set_title(text_params["title"], fontsize=text_params.get("label_fontsize", 14), pad=20)

    # 网格设置
    ax.grid(axis_params["grid"],
            linestyle=axis_params["grid_style"]["linestyle"],
            alpha=axis_params["grid_style"]["alpha"])

    # 刻度设置
    plt.xticks(rotation=axis_params["rotation"], fontsize=text_params.get("tick_fontsize", 12))
    plt.yticks(fontsize=text_params.get("tick_fontsize", 12))

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
