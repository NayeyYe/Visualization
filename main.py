import pandas as pd
from config import settings
from src.data_generator import generate_and_save_data

from src.matplot.area_plot import create_area_plot
from src.matplot.box_plot import create_box_plot
from src.matplot.calendar_hearmap import create_calendar_heatmap
from src.matplot.heatmap import create_heatmap
from src.matplot.line_plot import create_line_plot
from src.matplot.surface_3d import create_3d_surface

from src.pyeplot.calendar_heatmap import create_pye_calendar
from src.pyeplot.heatmap import create_pye_heatmap
from src.pyeplot.line_charts import create_pye_line
from src.pyeplot.surface_3d import create_pye_3dsurface


def mat_area_plot_generator():
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 生成matplotlib面积图
    create_area_plot(
        df=df.resample('D', on='timestamp').mean().reset_index(),
        config={
            "output": {"save_path": settings.MATPLOT_OUTPUT},
            "text": {"title": "2024年每日平均温度分布"}
        },
        show=False
    )

def mat_box_plot_generator():
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 自定义配置
    custom_config = {
        "text": {
            "title": "2024年月度温度分布",
            "title_fontsize": 20
        },
        "box": {
            "facecolor": "#2c7fb8",
            "flier_color": "#ff7f0e"
        },
        "output": {
            "save_path": settings.MATPLOT_OUTPUT,
            "filename": "monthly_temperature_box"
        }
    }

    create_box_plot(
        df=df,
        config=custom_config,
        group_by="month",
        show=True,
        box={"widths": 0.8}
    )

def mat_calendar_generator():
    df = pd.read_csv(settings.DATA_PATH)
    create_calendar_heatmap(
        df=df,
        config={
            "heatmap": {
                "cmap": "RdYlBu_r",
                "vmin": -15,
                "vmax": 45
            },
            "output": {
                "save_path": settings.MATPLOT_OUTPUT,
                "filename": "2024_temperature_calendar"
            }
        },
        year=2024,
        show=True
    )

def mat_heatmap_generator():
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)

    # 自定义配置
    custom_config = {
        "heatmap": {
            "cmap_colors": ["#006837", "#1a9850", "#a6d96a", "#fdae61", "#d7191c"],
            "vmin": -10,
            "vmax": 35
        },
        "output": {
            "save_path": settings.MATPLOT_OUTPUT,
            "filename": "hourly_heatmap"
        }
    }

    create_heatmap(
        df=df,
        config=custom_config,
        time_granularity="hour",
        show=True,
        text={"title": "2024年逐小时温度分布热力图"}
    )

def mat_line_chart_generator():
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])

    # 设置 'timestamp' 列为索引
    df.set_index('timestamp', inplace=True)

    # 重采样为每天的平均温度
    daily_avg_temp = df.resample('D').mean()

    # 重置索引以便后续处理
    daily_avg_temp.reset_index(inplace=True)

    # 创建自定义配置
    custom_config = {
        "text": {
            "title": "2024年温度变化趋势",
            "title_fontsize": 18,
            "label_fontsize": 14,
            "tick_fontsize": 12
        },
        "axis": {
            "xlabel": "日期",
            "ylabel": "温度(℃)",
            "date_format": "%m-%d",
            "rotation": 30
        },
        "line": {
            "color": "#d62728",
            "marker": "o",
            "markersize": 3
        },
        "legend": {
            "show": True,
            "label": "温度数据线",
            "loc": "upper left"
        },
        "output": {
            "save_path": settings.MATPLOT_OUTPUT,
            "filename": "custom_temperature_trend"
        }
    }

    # 调用绘图函数
    create_line_plot(
        df=daily_avg_temp,
        config=custom_config,
        show=True,
        # 也可以通过kwargs直接覆盖
        figure={"dpi": 800},
        line={"linewidth": 2.0}
    )

def mat_3d_surface_generator():
    df = pd.read_csv(settings.DATA_PATH)
    create_3d_surface(
        df=df,
        config={
            "surface": {
                "cmap": "viridis",
                "elevation": 30,
                "azimuth": -135
            },
            "output": {
                "save_path": settings.MATPLOT_OUTPUT,
                "filename": "3d_temp_surface_mat"
            }
        },
        show=True
    )

def pye_calendar_generator():
    df = pd.read_csv(settings.DATA_PATH)
    create_pye_calendar(
        df=df,
        config={
            "output_path": settings.PYECHARTS_OUTPUT,
            "range_colors": ["#f7fbff", "#c6dbef", "#6baed6", "#2171b5", "#08306b"]
        }
    )

def pye_heatmap_generator():
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)

    create_pye_heatmap(
        df=df,
        config={
            "output_path": settings.PYECHARTS_OUTPUT,
            "visualmap_colors": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
                                 "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
            "tooltip_formatter": "温度: {c} ℃<br/>日期: {b}<br/>小时: {a}"
        },
        time_granularity="hour"
    )

def pye_line_chart_generator():
    # 生成pyecharts折线图
    # 加载数据
    df = pd.read_csv(settings.DATA_PATH)
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    create_pye_line(
        df=df,
        config={
            "output_path": settings.PYECHARTS_OUTPUT,
            "width": "1800px",
            "height": "900px",
            "datazoom_range_start": 20,
            "datazoom_range_end": 80
        }
    )

def pye_3d_surface_generator():
    df = pd.read_csv(settings.DATA_PATH)
    create_pye_3dsurface(
        df=df,
        config={
            "output_path": settings.PYECHARTS_OUTPUT,
            "range_colors": ["#006837", "#1a9850", "#a6d96a", "#fdae61", "#d7191c"]
        }
    )

if __name__ == "__main__":
    generate_and_save_data()

    mat_area_plot_generator()
    mat_box_plot_generator()
    mat_calendar_generator()
    mat_heatmap_generator()
    mat_line_chart_generator()
    mat_3d_surface_generator()

    pye_calendar_generator()
    pye_heatmap_generator()
    pye_line_chart_generator()
    pye_3d_surface_generator()
