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
THRESHOLD = 0.1  # 阈值
WINDOW_SIZE = 120  # 滑动平均窗口（60分钟）
START_DATE = "2025-01-20"  # 绘图起始时间
END_DATE = "2025-02-20"  # 绘图结束时间

# 读取数据
df = pd.read_excel(FILE_PATH)
df[TIME_COL] = pd.to_datetime(df[TIME_COL])
df = df.set_index(TIME_COL).sort_index()


# 数据降噪处理
def denoise_data(series, threshold, window_size=4800):
    processed = series.copy()
    rolling_median = series.rolling(
        window=window_size, min_periods=1
    ).median()  # 滑动中位数
    valid_range = (rolling_median * (1 - threshold), rolling_median * (1 + threshold))
    mask = series.between(*valid_range)
    processed.loc[~mask] = np.nan
    return processed


processed = denoise_data(df[DATA_COL], THRESHOLD)

# 滑动平均处理
processed_filled = processed.interpolate()  # 线性插值填充缺失值
sma = processed_filled.rolling(window=WINDOW_SIZE, min_periods=1).mean()

# 将滑动平均结果按天重新采样并计算日均值
sma_daily = sma.resample("D").mean()

# 时间范围筛选
df_filtered = df.loc[START_DATE:END_DATE]
processed_filtered = processed.loc[START_DATE:END_DATE]
sma_filtered = sma.loc[START_DATE:END_DATE]
sma_daily_filtered = sma_daily.loc[START_DATE:END_DATE]

# 绘图设置
plt.figure(figsize=(14, 7), dpi=100)
ax = plt.gca()

# 绘制原始数据（散点图）
ax.scatter(
    df_filtered.index,
    df_filtered[DATA_COL],
    color="#D3D3D3",
    s=10,
    alpha=0.7,
    label="原始数据",
)

# 绘制处理数据（散点图）
ax.scatter(
    processed_filtered.index,
    processed_filtered,
    color="#FF4500",
    s=15,
    label=f"降噪数据（阈值{THRESHOLD*100:.0f}%）",
)

# 绘制滑动平均（折线图，保持为折线以显示趋势）
ax.plot(
    sma_filtered.index,
    sma_filtered,
    color="#1E90FF",
    linewidth=1.5,
    label=f"滑动平均（{WINDOW_SIZE}分钟窗口）",
)

# 绘制滑动平均的日均值（折线图）
ax.plot(
    sma_daily_filtered.index,
    sma_daily_filtered,
    color="#2E8B57",  # 使用绿色表示日均值
    linewidth=2,
    linestyle="--",
    label="滑动平均的日均值",
)

# 纵坐标设置
ax.set_ylim(0, 0.5)
ax.yaxis.set_major_locator(MultipleLocator(0.1))  # 主刻度每0.1
ax.yaxis.set_minor_locator(MultipleLocator(0.02))  # 次刻度每0.02
ax.yaxis.set_major_formatter("{x:.2f}")  # 保留两位小数

# 图表美化
ax.set_title(
    f"测量数据降噪处理对比\n(兴凯湖 {START_DATE} 至 {END_DATE})", pad=20, fontsize=14
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
    bbox_to_anchor=(0.18, 0.85),  # 调整垂直位置
    fontsize=10,
    handlelength=1.5,
    handletextpad=0.5,
)

plt.tight_layout()
plt.show()
