import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_temperature_data(seed=42):
    """
    生成模拟的365天*24小时温度数据
    :param seed: 随机种子保证可重复性
    :return: 包含时间戳和温度的DataFrame
    """
    np.random.seed(seed)

    # 生成时间序列
    start_date = datetime(2024, 1, 1)
    hours = 365 * 24
    timestamps = [start_date + timedelta(hours=h) for h in range(hours)]

    # 生成温度数据（年周期 + 日周期 + 噪声）
    t = np.arange(hours)
    yearly = 15 * np.sin(2 * np.pi * t / (365 * 24))  # 年周期
    daily = 10 * np.sin(2 * np.pi * t % 24 / 24)  # 日周期
    noise = np.random.normal(0, 3, hours)  # 随机噪声

    temperature = 5 + yearly + daily + noise
    return pd.DataFrame({"timestamp": timestamps, "temperature": temperature})
