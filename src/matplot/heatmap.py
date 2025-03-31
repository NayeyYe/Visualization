# src/matplot/heatmap.py
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from config.visualization_config import MATPLOT_HEATMAP_CONFIG
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


def create_heatmap(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        time_col: str = "timestamp",
        value_col: str = "temperature",
        time_granularity: str = "hour",  # 时间粒度 hour/month/day
        show: bool = False,
        **kwargs) -> None:
    """
    创建气温热力图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名称（默认'timestamp'）
    value_col : 数值列名称（默认'temperature'）
    time_granularity : 时间维度（hour/day/month）
    show : 是否显示图表（默认False）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_HEATMAP_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    heatmap_params = final_config["heatmap"]
    axis_params = final_config["axis"]
    text_params = final_config["text"]
    output_params = final_config["output"]

    # 数据预处理
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])

    # 创建时间维度矩阵
    if time_granularity == "hour":
        df["hour"] = df[time_col].dt.hour
        df["day"] = df[time_col].dt.dayofyear
        matrix = df.pivot_table(index="hour", columns="day", values=value_col)
    elif time_granularity == "day":
        df["day"] = df[time_col].dt.day
        df["month"] = df[time_col].dt.month
        matrix = df.pivot_table(index="day", columns="month", values=value_col)
    elif time_granularity == "month":
        df["month"] = df[time_col].dt.month
        df["year"] = df[time_col].dt.year
        matrix = df.pivot_table(index="month", columns="year", values=value_col)
    else:
        raise ValueError("time_granularity参数必须是hour/day/month")

    # 创建画布
    plt.figure(figsize=fig_params["figsize"], dpi=fig_params["dpi"])
    ax = plt.gca()

    # 创建自定义颜色映射
    cmap = LinearSegmentedColormap.from_list(
        "custom_cmap",
        heatmap_params["cmap_colors"],
        N=heatmap_params.get("cmap_levels", 256)
    )

    # 绘制热力图
    im = ax.imshow(
        matrix.values,
        aspect=heatmap_params.get("aspect_ratio"),
        cmap=cmap,
        vmin=heatmap_params["vmin"],
        vmax=heatmap_params["vmax"],
        interpolation=heatmap_params.get("interpolation")
    )

    # 设置坐标轴
    _set_axis_labels(ax, matrix, time_granularity, axis_params, text_params)

    # 添加颜色条
    cbar = plt.colorbar(im, fraction=0.023, pad=0.03)
    cbar.set_label(
        heatmap_params.get("cbar_label"),
        fontsize=text_params.get("label_fontsize")
    )
    cbar.ax.tick_params(labelsize=text_params["tick_fontsize"])

    # 设置标题
    ax.set_title(
        text_params["title"],
        fontsize=text_params["title_fontsize"],
        pad=20
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


def _set_axis_labels(ax, matrix, granularity, axis_params, text_params):
    """设置坐标轴标签"""
    # X轴设置
    if granularity == "hour":
        x_labels = [f"Day {i + 1}" for i in range(matrix.shape[1])]
        ax.set_xlabel(axis_params["xlabel"] or "Day of Year",
                      fontsize=text_params["label_fontsize"])
        ax.set_ylabel(axis_params["ylabel"] or "Hour",
                      fontsize=text_params["label_fontsize"])
        ax.set_yticks(np.arange(24))
        ax.set_yticklabels([f"{h:02d}:00" for h in range(24)])
    elif granularity == "day":
        ax.set_xlabel(axis_params["xlabel"] or "Month",
                      fontsize=text_params["label_fontsize"])
        ax.set_ylabel(axis_params["ylabel"] or "Day",
                      fontsize=text_params["label_fontsize"])
        ax.set_xticks(np.arange(12))
        ax.set_xticklabels([f"{m + 1}月" for m in range(12)])
    elif granularity == "month":
        ax.set_xlabel(axis_params["xlabel"] or "Year",
                      fontsize=text_params["label_fontsize"])
        ax.set_ylabel(axis_params["ylabel"] or "Month",
                      fontsize=text_params["label_fontsize"])
        ax.set_yticks(np.arange(12))
        ax.set_yticklabels([f"{m + 1}月" for m in range(12)])

    # 标签旋转设置
    plt.xticks(
        rotation=axis_params["x_rotation"],
        fontsize=text_params["tick_fontsize"]
    )
    plt.yticks(fontsize=text_params["tick_fontsize"])


def _update_nested_dict(original: dict, updates: dict) -> dict:
    """递归更新嵌套字典"""
    for key, value in updates.items():
        if isinstance(value, dict) and key in original:
            original[key] = _update_nested_dict(original[key], value)
        else:
            original[key] = value
    return original
