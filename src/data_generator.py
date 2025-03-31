# src/data_generator.py
from config import settings
from data.temperature import generate_temperature_data

def generate_and_save_data():
    """生成并保存模拟温度数据"""
    df = generate_temperature_data()
    df.to_csv(settings.DATA_PATH, index=False)
    print(f"数据已保存至：{settings.DATA_PATH}")

if __name__ == "__main__":
    generate_and_save_data()
