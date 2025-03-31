# src/pyeplot/calendar_heatmap.py
from typing import AnyStr

from pyecharts import options as opts
from pyecharts.charts import Calendar
import pandas as pd
from config.visualization_config import PYE_CALENDAR_CONFIG


def create_pye_calendar(
        df: pd.DataFrame,
        config: dict[str, AnyStr],
        date_col: str = "timestamp",
        value_col: str = "temperature",
        year: int = 2024,
        **kwargs) -> Calendar:
    """
    创建交互式日历热力图

    参数：
    df : 包含日期和温度的数据框
    config : 自定义配置字典
    date_col : 日期列名（默认'timestamp'）
    value_col : 温度列名（默认'temperature'）
    year : 要展示的年份（默认2024）
    kwargs : 支持配置项覆盖
    """
    # 合并配置参数
    final_config = {**PYE_CALENDAR_CONFIG, **(config or {})}
    final_config.update(kwargs)

    # 准备数据
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col])
    df = df[df[date_col].dt.year == year]
    data = [
        [d.strftime("%Y-%m-%d"), v]
        for d, v in zip(df[date_col], df[value_col])
    ]

    # 创建日历图
    calendar = Calendar(init_opts=opts.InitOpts(
        width=final_config["width"],
        height=final_config["height"],
        theme=final_config["theme"]
    ))

    calendar.add(
        series_name=final_config["series_name"],
        yaxis_data=data,
        calendar_opts=opts.CalendarOpts(
            range_=str(year),
            daylabel_opts=opts.CalendarDayLabelOpts(
                name_map="cn",
                margin=final_config["day_margin"]
            ),
            monthlabel_opts=opts.CalendarMonthLabelOpts(
                name_map="cn",
                margin=final_config["month_margin"]
            ),
            pos_left=final_config["pos_left"],
            pos_right=final_config["pos_right"],
            orient=final_config["orient"]
        )
    )

    calendar.set_global_opts(
        title_opts=opts.TitleOpts(
            title=final_config["title"],
            subtitle=final_config["subtitle"],
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=final_config["title_font_size"],
                color=final_config["title_color"]
            )
        ),
        visualmap_opts=opts.VisualMapOpts(
            min_=final_config["vmin"],
            max_=final_config["vmax"],
            orient=final_config["visualmap_orient"],
            pos_left=final_config["visualmap_pos_left"],
            pos_top=final_config["visualmap_pos_top"],
            range_color=final_config["range_colors"],
            is_piecewise=final_config["is_piecewise"]
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="item",
            formatter=final_config["tooltip_formatter"]
        )
    )

    # 保存输出
    if final_config["output_path"]:
        calendar.render(f"{final_config['output_path']}/{final_config['filename']}.html")

    return calendar
