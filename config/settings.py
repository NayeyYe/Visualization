import os


# 基础路径配置
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(BASE_DIR, 'data', 'temperature_data.csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'outputs')
MATPLOT_OUTPUT = os.path.join(OUTPUT_DIR, 'matplotlib')
PYECHARTS_OUTPUT = os.path.join(OUTPUT_DIR, 'pyecharts')

# 创建必要目录
os.makedirs(MATPLOT_OUTPUT, exist_ok=True)
os.makedirs(PYECHARTS_OUTPUT, exist_ok=True)

# 可视化配置
PLOT_CONFIG = {
    "figure_size": (12, 6),
    "line_style": "-",
    "color_palette": ["#1f77b4", "#ff7f0e", "#2ca02c"],
    "font_size": 12,
    "dpi": 300
}

print(BASE_DIR)
