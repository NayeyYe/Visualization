# src/matplot/calendar_heatmap.py
from typing import Optional, Dict, Any
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
from matplotlib.patches import Rectangle
from config.visualization_config import MATPLOT_CALENDAR_CONFIG


def create_calendar_heatmap(
        df: pd.DataFrame,
        config: Optional[Dict[str, Any]] = None,
        date_col: str = "timestamp",
        value_col: str = "temperature",
        year: int = 2024,
        show: bool = False,
        **kwargs) -> None:
    """
    创建日历热力图

    参数：
    df : 包含日期和温度的数据框
    config : 自定义配置字典
    date_col : 日期列名（默认'timestamp'）
    value_col : 温度列名（默认'temperature'）
    year : 要展示的年份（默认2024）
    show : 是否显示图表（默认False）
    kwargs : 支持任意配置项的覆盖
    """
    # 合并配置参数
    final_config = {**MATPLOT_CALENDAR_CONFIG, **(config or {})}
    final_config = _update_nested_dict(final_config, kwargs)

    # 解包配置参数
    fig_params = final_config["figure"]
    heatmap_params = final_config["heatmap"]
    text_params = final_config["text"]
    output_params = final_config["output"]

    # 数据预处理
    df = _prepare_calendar_data(df, date_col, value_col, year)

    # 创建画布
    fig = plt.figure(figsize=fig_params["figsize"], dpi=fig_params["dpi"])
    ax = fig.add_subplot(111)

    # 绘制日历
    _draw_calendar(ax, df, year, heatmap_params, text_params)

    # 设置颜色条
    _add_colorbar(fig, df[value_col], heatmap_params)

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


def _prepare_calendar_data(df, date_col, value_col, year):
    """准备日历数据"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[df[date_col].dt.year == year]

    # 创建完整日期索引
    full_dates = pd.date_range(start=f"{year}-01-01", end=f"{year}-12-31")
    return df.set_index(date_col).reindex(full_dates).reset_index()


def _draw_calendar(ax, df, year, heatmap_params, text_params):
    """绘制日历主体"""
    # 计算每周信息
    df['week'] = df['index'].dt.isocalendar().week
    df['day'] = df['index'].dt.day
    df['weekday'] = df['index'].dt.weekday  # Monday=0
    df['month'] = df['index'].dt.month

    # 颜色标准化
    norm = mpl.colors.Normalize(
        vmin=heatmap_params["vmin"],
        vmax=heatmap_params["vmax"]
    )
    cmap = mpl.cm.get_cmap(heatmap_params["cmap"])

    # 绘制每个日期方块
    for _, row in df.iterrows():
        if pd.isna(row['temperature']):
            continue

        # 计算方块位置
        week_number = row['week'] - df[df['month'] == row['month']]['week'].min()
        x_pos = (row['month'] - 1) * 3 + week_number // 4.5
        y_pos = row['weekday']

        # 绘制方块
        rect = Rectangle(
            (x_pos, y_pos),
            width=0.9,
            height=0.9,
            facecolor=cmap(norm(row['temperature'])),
            edgecolor='white'
        )
        ax.add_patch(rect)

        # 添加日期标签
        if heatmap_params.get("show_date", True):
            ax.text(
                x_pos + 0.45,
                y_pos + 0.45,
                str(row['day']),
                ha='center',
                va='center',
                fontsize=text_params["date_fontsize"],
                color=text_params["date_color"]
            )

    # 设置坐标轴
    ax.set_xlim(0, 12 * 3)
    ax.set_ylim(-0.5, 6.5)
    ax.invert_yaxis()

    # 设置月份标签
    for month in range(1, 13):
        ax.text(
            (month - 1) * 3 + 1.5,
            -0.3,
            f"{month}月",
            ha='center',
            fontsize=text_params["month_fontsize"]
        )

    # 设置星期标签
    weekdays = ["周一", "周二", "周三", "周四", "周五", "周六", "周日"]
    for i, day in enumerate(weekdays):
        ax.text(
            -0.5,
            i + 0.5,
            day,
            ha='right',
            va='center',
            fontsize=text_params["weekday_fontsize"]
        )

    # 隐藏坐标轴
    ax.axis('off')


def _add_colorbar(fig, values, heatmap_params):
    """添加颜色条"""
    norm = mpl.colors.Normalize(
        vmin=heatmap_params["vmin"],
        vmax=heatmap_params["vmax"]
    )
    cmap = mpl.cm.get_cmap(heatmap_params["cmap"])

    cbar_ax = fig.add_axes(heatmap_params.get("cbar_pos", [0.2, 0.08, 0.6, 0.03]))
    cb = mpl.colorbar.ColorbarBase(
        cbar_ax,
        cmap=cmap,
        norm=norm,
        orientation='horizontal'
    )
    cb.set_label(
        heatmap_params.get("cbar_label"),
        fontsize=heatmap_params.get("cbar_fontsize")
    )


def _update_nested_dict(original: dict, updates: dict) -> dict:
    """递归更新嵌套字典"""
    for key, value in updates.items():
        if isinstance(value, dict) and key in original:
            original[key] = _update_nested_dict(original[key], value)
        else:
            original[key] = value
    return original
