# src/matplot/area_plot.py
from config.visualization_config import MATPLOT_AREA_CONFIG
from typing import Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from pylab import mpl

mpl.rcParams["font.sans-serif"] = ["SimHei"]
mpl.rcParams["axes.unicode_minus"] = False


def create_area_plot(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        time_col: str = "timestamp",
        value_col: str = "temperature",
        show: bool = False,
        **kwargs) -> None:
    """
    创建气温面积图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名称（默认'timestamp'）
    value_col : 数值列名称（默认'temperature'）
    show : 是否显示图表（默认False）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_AREA_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    area_params = final_config["area"]
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

    # 绘制面积图
    ax.fill_between(
        dates,
        values,
        color=area_params["fill_color"],
        alpha=area_params["alpha"],
        linewidth=area_params["linewidth"],
        linestyle=area_params["linestyle"],
        edgecolor=area_params["edge_color"],
        label=legend_params["label"]
    )

    # 坐标轴设置
    ax.set_xlabel(axis_params["xlabel"], fontsize=text_params.get("label_fontsize"))
    ax.set_ylabel(axis_params["ylabel"], fontsize=text_params.get("label_fontsize"))
    ax.set_title(text_params["title"], fontsize=text_params.get("title_fontsize"), pad=20)

    # 日期格式化
    locator = mdates.AutoDateLocator()
    formatter = mdates.DateFormatter(axis_params["date_format"])
    ax.xaxis.set_major_locator(locator)
    ax.xaxis.set_major_formatter(formatter)

    # 刻度设置
    plt.xticks(rotation=axis_params["rotation"], ha='right')
    ax.tick_params(axis='both', labelsize=text_params.get("tick_fontsize"))

    # 保存输出
    filename = output_params.get("filename")
    if output_params["save_path"]:
        plt.savefig(
            f"{output_params['save_path']}/temperature_area_plot.png",
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