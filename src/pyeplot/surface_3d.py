# src/pyeplot/3d_surface.py
from typing import AnyStr

from pyecharts import options as opts
from pyecharts.charts import Surface3D
import pandas as pd
import numpy as np
from config.visualization_config import PYE_3DSURFACE_CONFIG


def create_pye_3dsurface(
        df: pd.DataFrame,
        config: dict[str, AnyStr] = None,
        date_col: str = "timestamp",
        value_col: str = "temperature",
        year: int = 2024,
        **kwargs) -> Surface3D:
    """
    创建交互式3D曲面图

    参数：
    df : 包含时间序列数据的数据框
    config : 自定义配置字典
    date_col : 日期列名（默认'timestamp'）
    value_col : 温度列名（默认'temperature'）
    year : 要展示的年份（默认2024）
    kwargs : 支持配置项覆盖
    """
    # 合并配置参数
    final_config = {**PYE_3DSURFACE_CONFIG, **(config or {})}
    final_config.update(kwargs)

    # 数据预处理
    df = _prepare_pye3d_data(df, date_col, year)

    # 生成网格数据
    days = df['day_of_year'].unique()
    hours = df['hour'].unique()
    X, Y = np.meshgrid(days, hours)
    Z = df.pivot(index='hour', columns='day_of_year', values=value_col).values

    # 转换为Pyecharts数据格式
    data = []
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            data.append([int(X[i, j]), int(Y[i, j]), round(float(Z[i, j]), 1)])

    # 创建3D曲面图
    surface = Surface3D(init_opts=opts.InitOpts(
        width=final_config["width"],
        height=final_config["height"],
        theme=final_config["theme"]
    ))

    surface.add(
        series_name=final_config["series_name"],
        shading=final_config["shading"],
        data=data,
        xaxis3d_opts=opts.Axis3DOpts(
            name=final_config["xaxis_name"],
            type_="value",
            min_=1,
            max_=366,
            splitline_opts=opts.SplitLineOpts(is_show=False)
        ),
        yaxis3d_opts=opts.Axis3DOpts(
            name=final_config["yaxis_name"],
            type_="value",
            min_=0,
            max_=23,
            splitline_opts=opts.SplitLineOpts(is_show=False)
        ),
        zaxis3d_opts=opts.Axis3DOpts(
            name=final_config["zaxis_name"],
            type_="value",
            splitline_opts=opts.SplitLineOpts(is_show=False)
        ),
    )

    surface.set_global_opts(
        title_opts=opts.TitleOpts(
            title=final_config["title"],
            subtitle=final_config["subtitle"],
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=final_config["title_font_size"],
                color=final_config["title_color"]
            )
        ),
        visualmap_opts=opts.VisualMapOpts(
            dimension=2,
            min_=final_config["vmin"],
            max_=final_config["vmax"],
            range_color=final_config["range_colors"],
            pos_left=final_config["visualmap_pos_left"],
            pos_top=final_config["visualmap_pos_top"]
        ),
        tooltip_opts=opts.TooltipOpts(
            formatter=final_config["tooltip_formatter"]
        )
    )

    # 保存输出
    if final_config["output_path"]:
        surface.render(f"{final_config['output_path']}/{final_config['filename']}.html")

    return surface


def _prepare_pye3d_data(df, date_col, year):
    """准备Pyecharts 3D数据"""
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[df[date_col].dt.year == year]
    df['day_of_year'] = df[date_col].dt.dayofyear
    df['hour'] = df[date_col].dt.hour
    return df.sort_values(['day_of_year', 'hour'])
