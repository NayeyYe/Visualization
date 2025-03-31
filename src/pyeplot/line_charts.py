# src/pyeplot/line_chart.py
from pyecharts import options as opts
from pyecharts.charts import Line
from pyecharts.commons.utils import JsCode
import pandas as pd
from config.visualization_config import PYE_LINE_CONFIG


def create_pye_line(
        df: pd.DataFrame,
        config: dict = None,
        time_col: str = "timestamp",
        value_col: str = "temperature",
        **kwargs) -> Line:
    """
    创建交互式温度折线图

    参数：
    df : 包含时间温度数据的数据框
    config : 自定义配置字典（可选）
    time_col : 时间列名（默认'timestamp'）
    value_col : 数值列名（默认'temperature'）
    kwargs : 支持配置项覆盖
    """
    # 合并配置参数
    final_config = {**PYE_LINE_CONFIG, **(config or {})}
    final_config.update(kwargs)

    # 处理数据
    dates = df[time_col].dt.strftime(final_config["date_format"]).tolist()
    values = df[value_col].round(2).tolist()

    # 初始化图表
    line_chart = Line(init_opts=opts.InitOpts(
        width=final_config["width"],
        height=final_config["height"],
        theme=final_config["theme"]
    ))

    # 添加数据
    line_chart.add_xaxis(xaxis_data=dates)
    line_chart.add_yaxis(
        series_name=final_config["series_name"],
        y_axis=values,
        is_smooth=final_config["is_smooth"],
        symbol=final_config["symbol"],
        symbol_size=final_config["symbol_size"],
        color=final_config["line_color"],
        label_opts=opts.LabelOpts(is_show=final_config["show_label"]),
        linestyle_opts=opts.LineStyleOpts(
            width=final_config["line_width"],
            type_=final_config["line_type"]
        ),
        areastyle_opts=opts.AreaStyleOpts(
            opacity=final_config["area_opacity"],
            color=JsCode(final_config["area_color_js"])
        )
    )

    # 设置全局配置
    line_chart.set_global_opts(
        title_opts=opts.TitleOpts(
            title=final_config["title"],
            subtitle=final_config["subtitle"],
            title_textstyle_opts=opts.TextStyleOpts(
                font_size=final_config["title_font_size"],
                color=final_config["title_color"]
            )
        ),
        tooltip_opts=opts.TooltipOpts(
            trigger="axis",
            axis_pointer_type="cross",
            background_color="rgba(245,245,245,0.8)",
            border_width=1,
            border_color="#ccc"
        ),
        xaxis_opts=opts.AxisOpts(
            type_="category",
            name=final_config["xaxis_name"],
            axislabel_opts=opts.LabelOpts(
                rotate=final_config["xaxis_rotate"],
                font_size=final_config["xaxis_font_size"]
            )
        ),
        yaxis_opts=opts.AxisOpts(
            type_="value",
            name=final_config["yaxis_name"],
            axislabel_opts=opts.LabelOpts(
                font_size=final_config["yaxis_font_size"]
            ),
            splitline_opts=opts.SplitLineOpts(is_show=True)
        ),
        datazoom_opts=[
            opts.DataZoomOpts(
                range_start=final_config["datazoom_range_start"],
                range_end=final_config["datazoom_range_end"]
            ),
            opts.DataZoomOpts(type_="inside")
        ],
        legend_opts=opts.LegendOpts(
            pos_left="20%",
            pos_top="5%",
            orient="horizontal"
        )
    )

    # 保存输出
    if final_config["output_path"]:
        line_chart.render(f"{final_config['output_path']}/{final_config['filename']}.html")

    return line_chart