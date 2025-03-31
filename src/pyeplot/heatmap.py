# src/pyeplot/heatmap.py
from typing import AnyStr

from pyecharts import options as opts
from pyecharts.charts import HeatMap
import pandas as pd
from config.visualization_config import PYE_HEATMAP_CONFIG


def create_pye_heatmap(
        df: pd.DataFrame,
        config : dict[str, AnyStr],
        time_col: str = "timestamp",
        value_col: str = "temperature",
        time_granularity: str = "hour",
        **kwargs) -> HeatMap:
    """
    创建交互式气温热力图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名称（默认'timestamp'）
    value_col : 数值列名称（默认'temperature'）
    time_granularity : 时间维度（hour/day/month）
    kwargs : 支持配置项覆盖
    """
    # 合并配置参数
    final_config = {**PYE_HEATMAP_CONFIG, **(config or {})}
    final_config.update(kwargs)

    # 数据预处理
    df = df.copy()
    df[time_col] = pd.to_datetime(df[time_col])

    # 生成坐标数据
    if time_granularity == "hour":
        df["x_axis"] = df[time_col].dt.dayofyear
        df["y_axis"] = df[time_col].dt.hour
        x_label = "Day of Year"
        y_label = "Hour"
    elif time_granularity == "day":
        df["x_axis"] = df[time_col].dt.month
        df["y_axis"] = df[time_col].dt.day
        x_label = "Month"
        y_label = "Day"
    elif time_granularity == "month":
        df["x_axis"] = df[time_col].dt.year
        df["y_axis"] = df[time_col].dt.month
        x_label = "Year"
        y_label = "Month"
    else:
        raise ValueError("time_granularity参数必须是hour/day/month")

    # 生成热力数据
    data = [
        [int(row["x_axis"]), int(row["y_axis"]), float(row[value_col])]
        for _, row in df.iterrows()
    ]

    # 创建热力图
    heatmap = HeatMap(init_opts=opts.InitOpts(
        width=final_config["width"],
        height=final_config["height"],
        theme=final_config["theme"]
    ))

    heatmap.add_xaxis(
        xaxis_data=sorted(df["x_axis"].unique().astype(int)))
    heatmap.add_yaxis(
        series_name=final_config["series_name"],
        yaxis_data=sorted(df["y_axis"].unique().astype(int)),
        value=data,
        label_opts=opts.LabelOpts(
            is_show=final_config["show_label"],
            position="inside"
        )
    )

    # 设置全局配置
    heatmap.set_global_opts(
        title_opts=opts.TitleOpts(
            title=final_config["title"],
            subtitle=final_config["subtitle"],
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=final_config["title_font_size"],
                color=final_config["title_color"]
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            formatter=final_config["tooltip_formatter"],
            background_color="rgba(0,0,0,0.7)",
            border_color="#ccc",
            textstyle_opts=opts.TextStyleOpts(color="#fff")
        ),
        xaxis_opts=opts.AxisOpts(
            name=x_label,
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(is_show=True),
            axislabel_opts=opts.LabelOpts(
                rotate=final_config["x_rotate"],
                font_size=final_config["x_font_size"]
            )
        ),
        yaxis_opts=opts.AxisOpts(
            name=y_label,
            type_="category",
            splitarea_opts=opts.SplitAreaOpts(is_show=True),
            axislabel_opts=opts.LabelOpts(
                font_size=final_config["y_font_size"]
            )
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=final_config["visualmap_min"],
            max_=final_config["visualmap_max"],
            orient=final_config["visualmap_orient"],
            pos_left=final_config["visualmap_pos_left"],
            pos_top=final_config["visualmap_pos_top"],
            range_color=final_config["visualmap_colors"],
            is_piecewise=final_config["is_piecewise"]
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=final_config["datazoom_range_start"],
                range_end=final_config["datazoom_range_end"]
            )
        ]
    )

    # 保存输出
    if final_config["output_path"]:
        heatmap.render(f"{final_config['output_path']}/{final_config['filename']}.html")

    return heatmap
