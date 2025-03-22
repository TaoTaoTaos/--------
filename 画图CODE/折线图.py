import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
import matplotlib.dates as mdates

plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

# 参数配置
FILE_PATH = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x数据\CR1000X处理后数据\CR1000X平均数据(每分钟).xlsx"
DATA_COL = "高度计（冰厚）"  # 修改后的数据列名
TIME_COL = "时间"
THRESHOLD = 0.4  # 30%阈值

# 读取数据
df = pd.read_excel(FILE_PATH)
df[TIME_COL] = pd.to_datetime(df[TIME_COL])
df = df.set_index(TIME_COL).sort_index()


# 数据降噪处理（保持原有逻辑）
def denoise_data(series, threshold):
    processed = series.copy()
    for day in pd.date_range(
        start=series.index.min().date(), end=series.index.max().date(), freq="D"
    ):
        daily_data = series[day.strftime("%Y-%m-%d")]
        if len(daily_data) == 0:
            continue
        avg = daily_data.mean()
        valid_range = (avg * (1 - threshold), avg * (1 + threshold))
        mask = daily_data.between(*valid_range)
        processed.loc[daily_data[~mask].index] = np.nan
    return processed


processed = denoise_data(df[DATA_COL], THRESHOLD)

# 绘图设置
plt.figure(figsize=(14, 7), dpi=100)
ax = plt.gca()

# 绘制原始数据
ax.plot(
    df.index, df[DATA_COL], color="#D3D3D3", linewidth=0.8, alpha=0.7, label="原始数据"
)

# 绘制处理数据
ax.plot(
    processed.index,
    processed,
    color="#FF4500",
    linewidth=1.2,
    label=f"降噪数据（阈值{THRESHOLD*100:.0f}%）",
)

# 纵坐标设置
ax.set_ylim(0, 0.5)
ax.yaxis.set_major_locator(MultipleLocator(0.1))  # 主刻度每0.1
ax.yaxis.set_minor_locator(MultipleLocator(0.02))  # 次刻度每0.02
ax.yaxis.set_major_formatter("{x:.2f}")  # 保留两位小数

# 图表美化
ax.set_title(
    "测量数据降噪处理对比\n(兴凯湖 2025-01-18至2025-02-16)", pad=20, fontsize=14
)
ax.set_xlabel("日期", labelpad=12)
ax.set_ylabel("测量值", labelpad=12)
ax.grid(which="major", linestyle="--", alpha=0.7)
ax.grid(which="minor", linestyle=":", alpha=0.4)
ax.tick_params(axis="both", which="both", length=4)

# 日期格式化
ax.xaxis.set_major_formatter(mdates.ConciseDateFormatter(ax.xaxis.get_major_locator()))

# 图例优化
handles, labels = ax.get_legend_handles_labels()
ax.legend(
    handles,
    labels,
    frameon=False,
    bbox_to_anchor=(0.18, 0.95),
    fontsize=10,
    handlelength=1.5,
    handletextpad=0.5,
)

plt.tight_layout()
plt.show()
