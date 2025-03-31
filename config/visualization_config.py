"""
可视化配置参数中心
存放matplotlib/pyecharts等可视化工具的参数配置
"""

# ========== Matplotlib 面积图默认配置 ==========
MATPLOT_AREA_CONFIG = {
    "figure": {
        "figsize": (16, 8),
        "dpi": 300
    },
    "area": {
        "fill_color": "#4c72b0",
        "alpha": 0.3,
        "linewidth": 1.2,
        "linestyle": "--",
        "edge_color": "#2c5f8b"
    },
    "axis": {
        "xlabel": "日期",
        "ylabel": "温度(℃)",
        "date_format": "%Y-%m",
        "rotation": 45,
        "grid": True,
        "grid_style": {"linestyle": ":", "alpha": 0.4}
    },
    "text": {
        "title": "温度分布面积图",
        "title_fontsize": 18,
        "label_fontsize": 14,
        "tick_fontsize": 12
    },
    "legend": {
        "show": True,
        "label": "温度分布",
        "loc": "upper left",
        "fontsize": 12
    },
    "output": {
        "save_path": None,
        "filename": "temperature_area_plot",
        "save_dpi": 300
    }
}

# ========== Matplotlib 箱线图默认配置 ==========
MATPLOT_BOX_CONFIG = {
    "figure": {
        "figsize": (16, 8),
        "dpi": 300
    },
    "box": {
        "patch_artist": True,
        "show_means": True,
        "show_fliers": True,
        "widths": 0.6,
        "facecolor": "#4c72b0",
        "alpha": 0.8,
        "edgecolor": "#2c3e50",
        "linewidth": 1.5,
        "flier_marker": "o",
        "flier_size": 4,
        "flier_color": "#d62728",
        "flier_alpha": 0.5
    },
    "axis": {
        "xlabel": None,
        "ylabel": "Temperature (°C)",
        "grid": True,
        "grid_style": {"linestyle": "--", "alpha": 0.6},
        "rotation": 45
    },
    "text": {
        "title": "温度分布箱线图",
        "title_fontsize": 18,
        "label_fontsize": 14,
        "tick_fontsize": 12
    },
    "output": {
        "save_path": None,
        "filename": "temperature_box_plot",
        "save_dpi": 300
    }
}

# ========== Matplotlib 日历热力图配置 ==========
MATPLOT_CALENDAR_CONFIG = {
    "figure": {
        "figsize": (24, 12),
        "dpi": 300
    },
    "heatmap": {
        "cmap": "YlOrRd",
        "vmin": -10,
        "vmax": 40,
        "show_date": True,
        "cbar_label": "温度 (°C)",
        "cbar_fontsize": 12,
        "cbar_pos": [0.2, 0.08, 0.6, 0.03]
    },
    "text": {
        "month_fontsize": 12,
        "weekday_fontsize": 10,
        "date_fontsize": 6,
        "date_color": "#333333"
    },
    "output": {
        "save_path": None,
        "filename": "mat_calendar_heatmap",
        "save_dpi": 300
    }
}

# ========== Matplotlib 热力图默认配置 ==========
MATPLOT_HEATMAP_CONFIG = {
    "figure": {
        "figsize": (20, 8),
        "dpi": 300
    },
    "heatmap": {
        "cmap_colors": ["#2b8cbe", "#a6bddb", "#f0f0f0", "#fdbb84", "#e34a33"],
        "cmap_levels": 256,
        "aspect_ratio": "auto",
        "vmin": -20,
        "vmax": 40,
        "interpolation": "nearest",
        "cbar_label": "Temperature (°C)"
    },
    "axis": {
        "xlabel": None,
        "ylabel": None,
        "x_rotation": 45,
        "grid": False
    },
    "text": {
        "title": "小时级温度热力图",
        "title_fontsize": 18,
        "label_fontsize": 14,
        "tick_fontsize": 12
    },
    "output": {
        "save_path": None,
        "filename": "temperature_heatmap",
        "save_dpi": 300
    }
}

# ========== Matplotlib 折线图默认配置 ==========
MATPLOT_LINE_CONFIG = {
    "figure": {
        "figsize": (14, 7),
        "dpi": 300
    },
    "line": {
        "color": "#2c7fb8",
        "linestyle": "-",
        "linewidth": 1.5,
        "alpha": 0.8,
        "marker": None,
        "markersize": 4
    },
    "axis": {
        "xlabel": "Date",
        "ylabel": "Temperature (°C)",
        "date_format": "%Y-%m",
        "rotation": 45,
        "grid": True,
        "grid_style": {"linestyle": "--", "alpha": 0.6}
    },
    "text": {
        "title": "Hourly Temperature Trend",
        "title_fontsize": 16,
        "label_fontsize": 12,
        "tick_fontsize": 10
    },
    "legend": {
        "show": False,
        "label": None,
        "loc": "upper right",
        "fontsize": 12
    },
    "output": {
        "save_path": None,
        "filename": "temperature_line_plot",
        "save_dpi": 300
    }
}

# ========== Matplotlib 3D曲面图配置 ==========
MATPLOT_3DSURFACE_CONFIG = {
    "figure": {
        "figsize": (16, 10),
        "dpi": 300
    },
    "surface": {
        "cmap": "coolwarm",
        "rstride": 3,
        "cstride": 10,
        "alpha": 0.8,
        "linewidth": 0.5,
        "antialiased": True,
        "cbar_label": "Temperature (°C)",
        "cbar_fontsize": 12,
        "elevation": 25,
        "azimuth": -120
    },
    "axis": {
        "xlabel": "日期",
        "ylabel": "小时",
        "zlabel": "温度(℃)",
        "label_pad": 15
    },
    "text": {
        "title": "全年温度三维分布",
        "title_fontsize": 18,
        "label_fontsize": 14,
        "tick_fontsize": 10,
        "title_ypos": 0.92
    },
    "output": {
        "save_path": None,
        "filename": "3d_temperature_surface",
        "save_dpi": 300
    }
}

# ========== pyecharts 日历热力图配置 ==========
PYE_CALENDAR_CONFIG = {
    "width": "1800px",
    "height": "1000px",
    "theme": "light",
    "series_name": "每日温度",
    "title": "2024年温度日历图",
    "subtitle": "数据来源：模拟数据 | 单位：℃",
    "title_font_size": 22,
    "title_color": "#2c343c",
    "day_margin": 30,
    "month_margin": 30,
    "pos_left": "100px",
    "pos_right": "60px",
    "orient": "horizontal",
    "vmin": -10,
    "vmax": 40,
    "visualmap_orient": "vertical",
    "visualmap_pos_left": "50px",
    "visualmap_pos_top": "center",
    "range_colors": ["#f0f9e8", "#bae4bc", "#7bccc4", "#43a2ca", "#0868ac"],
    "is_piecewise": True,
    "tooltip_formatter": "日期: {b}<br/>温度: {c}℃",
    "output_path": None,
    "filename": "pye_calendar_heatmap"
}

# ========== pyecharts 热力图默认配置 ==========
PYE_HEATMAP_CONFIG = {
    "width": "2000px",
    "height": "800px",
    "theme": "dark",
    "series_name": "温度分布",
    "show_label": False,
    "title": "全年温度分布热力图",
    "subtitle": "数据来源：模拟数据 | 单位：℃",
    "title_font_size": 22,
    "title_color": "#ffffff",
    "x_rotate": 45,
    "x_font_size": 12,
    "y_font_size": 14,
    "visualmap_min": -20,
    "visualmap_max": 40,
    "visualmap_orient": "vertical",
    "visualmap_pos_left": "93%",
    "visualmap_pos_top": "center",
    "visualmap_colors": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
                        "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
    "is_piecewise": True,
    "tooltip_formatter": "温度: {c} ℃<br/>X轴: {b}<br/>Y轴: {a}",
    "datazoom_range_start": 0,
    "datazoom_range_end": 100,
    "output_path": None,
    "filename": "pye_temperature_heatmap"
}

# ========== pyecharts 折线图默认配置 ==========
PYE_LINE_CONFIG = {
    "width": "1600px",
    "height": "800px",
    "theme": "light",
    "series_name": "温度数据",
    "is_smooth": True,
    "symbol": "circle",
    "symbol_size": 6,
    "line_color": "#c23531",
    "line_width": 2,
    "line_type": "solid",
    "area_opacity": 0.1,
    "area_color_js": "new echarts.graphic.LinearGradient(0, 0, 0, 1, [{offset: 0, color: 'rgba(204,51,51,0.8)'}, {offset: 1, color: 'rgba(204,51,51,0)'}])",
    "title": "全年温度变化趋势",
    "subtitle": "数据来源：模拟数据",
    "title_font_size": 22,
    "title_color": "#2c343c",
    "xaxis_name": "日期",
    "yaxis_name": "温度(℃)",
    "xaxis_rotate": 30,
    "xaxis_font_size": 12,
    "yaxis_font_size": 14,
    "show_label": False,
    "date_format": "%Y-%m-%d",
    "datazoom_range_start": 0,
    "datazoom_range_end": 100,
    "output_path": None,
    "filename": "pye_temperature_line"
}

# ========== pyecharts 3D曲面图配置 ==========
PYE_3DSURFACE_CONFIG = {
    "width": "1600px",
    "height": "900px",
    "theme": "dark",
    "series_name": "温度曲面",
    "shading": "color",
    "xaxis_name": "Day of Year",
    "yaxis_name": "Hour",
    "zaxis_name": "Temperature",
    "title": "三维温度曲面图",
    "subtitle": "数据来源：模拟数据 | 单位：℃",
    "title_font_size": 22,
    "title_color": "#ffffff",
    "vmin": -10,
    "vmax": 40,
    "range_colors": ["#313695", "#4575b4", "#74add1", "#abd9e9", "#e0f3f8",
                    "#fee090", "#fdae61", "#f46d43", "#d73027", "#a50026"],
    "visualmap_pos_left": "5%",
    "visualmap_pos_top": "center",
    "tooltip_formatter": "日期: {x}天<br/>时刻: {y}时<br/>温度: {z}℃",
    "output_path": None,
    "filename": "3d_temperature_surface"
}
