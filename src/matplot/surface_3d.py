# src/matplot/3d_surface.py
from typing import Optional, Dict, Any
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from config.visualization_config import MATPLOT_3DSURFACE_CONFIG


def create_3d_surface(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        date_col: str = "timestamp",
        value_col: str = "temperature",
        year: int = 2024,
        show: bool = False,
        **kwargs) -> None:
    """
    创建时间-小时-温度三维曲面图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典
    date_col : 日期列名（默认'timestamp'）
    value_col : 温度列名（默认'temperature'）
    year : 要展示的年份（默认2024）
    show : 是否显示图表（默认False）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_3DSURFACE_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    surface_params = final_config["surface"]
    axis_params = final_config["axis"]
    text_params = final_config["text"]
    output_params = final_config["output"]

    # 数据预处理
    df = _prepare_3d_data(df, date_col, year)

    # 创建网格数据
    days = df['day_of_year'].unique()
    hours = df['hour'].unique()
    X, Y = np.meshgrid(days, hours)
    Z = df.pivot(index='hour', columns='day_of_year', values=value_col).values

    # 创建画布
    fig = plt.figure(figsize=fig_params["figsize"], dpi=fig_params["dpi"])
    ax = fig.add_subplot(111, projection='3d')

    # 绘制曲面
    surf = ax.plot_surface(
        X, Y, Z,
        cmap=surface_params["cmap"],
        rstride=surface_params.get("rstride", 3),
        cstride=surface_params.get("cstride", 10),
        alpha=surface_params.get("alpha"),
        linewidth=surface_params.get("linewidth"),
        antialiased=surface_params.get("antialiased", True)
    )

    # 设置坐标轴
    _set_3d_axes(ax, days, hours, Z, axis_params, text_params, year)

    # 添加颜色条
    cbar = fig.colorbar(surf, shrink=0.5, aspect=10)
    cbar.set_label(
        surface_params.get("cbar_label"),
        fontsize=text_params.get("cbar_fontsize")
    )

    # 设置视角
    ax.view_init(
        elev=surface_params["elevation"],
        azim=surface_params["azimuth"]
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


def _prepare_3d_data(df, date_col, year):
    """准备3D曲面数据"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[df[date_col].dt.year == year]
    df['day_of_year'] = df[date_col].dt.dayofyear
    df['hour'] = df[date_col].dt.hour
    return df.sort_values(['day_of_year', 'hour'])


def _set_3d_axes(ax, days, hours, Z, axis_params, text_params, year):
    """设置3D坐标轴"""
    # X轴（日期）
    x_ticks = np.linspace(1, max(days), 12)
    ax.set_xticks(x_ticks)
    date_labels = [(pd.Timestamp(f"{year}-01-01") + pd.DateOffset(days=int(d - 1))).strftime("%b") for d in x_ticks]

    ax.set_xticklabels(
        date_labels,
        fontsize=text_params["tick_fontsize"]
    )
    ax.set_xlabel(
        axis_params["xlabel"],
        fontsize=text_params["label_fontsize"],
        labelpad=axis_params["label_pad"]
    )

    # Y轴（小时）
    ax.set_yticks(np.arange(0, 24, 3))
    ax.set_yticklabels(
        [f"{h:02d}:00" for h in range(0, 24, 3)],
        fontsize=text_params["tick_fontsize"]
    )
    ax.set_ylabel(
        axis_params["ylabel"],
        fontsize=text_params["label_fontsize"],
        labelpad=axis_params["label_pad"]
    )

    # Z轴（温度）
    z_min = np.nanmin(Z)
    z_max = np.nanmax(Z)
    ax.set_zlim(z_min, z_max)
    ax.set_zlabel(
        axis_params["zlabel"],
        fontsize=text_params["label_fontsize"],
        labelpad=axis_params["label_pad"]
    )

    # 标题
    ax.set_title(
        text_params["title"],
        fontsize=text_params["title_fontsize"],
        y=text_params["title_ypos"]
    )


def _update_nested_dict(original: dict, updates: dict) -> dict:
    """递归更新嵌套字典"""
    for key, value in updates.items():
        if isinstance(value, dict) and key in original:
            original[key] = _update_nested_dict(original[key], value)
        else:
            original[key] = value
    return original
