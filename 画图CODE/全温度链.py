import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import interpolate
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.ticker import MultipleLocator  # 新增刻度控制

# ================= 参数配置区域 =================

SELECTED_COLS = [
    "CR温度1",
    "CR温度2",
    "温度9 (℃)",
    "温度8 (℃)",
    "温度7 (℃)",
    "温度6 (℃)",
    "温度5 (℃)",
    "温度4 (℃)",
    "温度3 (℃)",
    "温度2 (℃)",
    "温度1 (℃)",
]

DEPTHS = [-0, -0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, -1.8, -2]  # 单位：米
INTERP_DEPTH_STEP = 0.001  # 插值步长 (米)
VMIN = -18
VMAX = 5
TICK_STEP = 3  # 颜色条主刻度间隔 (℃)
DATE_TICKS = 5  # 日期刻度数量

# 颜色定义，
COLORS = [
    (-18, "#0000FF"),  # 深蓝
    (-12, "#00FFFF"),  # 皇家蓝
    (-6, "#5deb69"),  # 天蓝
    (0, "#FFFF00"),  # 黄色
    (5, "#FF0000"),  # 红色
]

# 间距控制参数（单位：磅）
SPACING = {
    "xlabel_pad": 15,
    "ylabel_pad": 20,
    "xtick_pad": 10,
    "ytick_pad": 8,
    "cbar_label_pad": 15,
    "cbar_tick_pad": 8,
}

plt.rcParams["axes.unicode_minus"] = False
# ===============================================

# 设置中文字体
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

# 读取数据
data_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\两个平台结合后的数据\逐分钟温度链数据(2.9) 修复温度5.xlsx"
df = pd.read_excel(data_path)

# 时间序列处理
df["时间"] = pd.to_datetime(df["时间"])
df.set_index("时间", inplace=True)

# 数据预处理
df_temp = df[SELECTED_COLS].copy().astype(float)

# 创建插值后的深度序列
new_depths = np.arange(DEPTHS[0], DEPTHS[-1] - INTERP_DEPTH_STEP, -INTERP_DEPTH_STEP)
interp_matrix = []

# 对每个时间点进行三次样条插值
for timestamp in df_temp.index:
    depths_sorted = sorted(DEPTHS)
    values_sorted = [df_temp.loc[timestamp, col] for col in reversed(SELECTED_COLS)]
    f = interpolate.interp1d(
        depths_sorted, values_sorted, kind="cubic", fill_value="extrapolate"
    )
    interp_values = f(new_depths)
    interp_matrix.append(interp_values)

# 构建插值后的DataFrame
df_interp = pd.DataFrame(
    np.array(interp_matrix).T,
    index=[f"{abs(d)*100:.0f}cm" for d in new_depths],
    columns=df_temp.index,
).T

# 创建自定义颜色映射
temp_range = VMAX - VMIN
color_stops = [(t - VMIN) / temp_range for t, _ in COLORS]
cmap_custom = LinearSegmentedColormap.from_list(
    "BlueWhiteRed",
    list(zip(color_stops, [c[1] for c in COLORS])),
)

# 绘制热力图
plt.figure(figsize=(17, 9))
ax = sns.heatmap(
    df_interp.T,
    cmap=cmap_custom,
    cbar_kws={
        "label": "温度 (℃)",
        "shrink": 0.8,
        "aspect": 20,
        "pad": 0.03,
    },
    vmin=VMIN,
    vmax=VMAX,
    yticklabels=False,
    xticklabels=False,
)

# 设置坐标轴标签
ax.set_xlabel("日期", fontsize=12, labelpad=SPACING["xlabel_pad"])
ax.set_ylabel("深度 (cm)", fontsize=13, labelpad=SPACING["ylabel_pad"])

# 设置y轴刻度
original_positions = [np.abs(new_depths - d).argmin() for d in DEPTHS]
ax.set_yticks(original_positions)
ax.set_yticklabels([f"{int(abs(d)*100)}cm" for d in DEPTHS], fontsize=12)

# 设置左侧y轴刻度样式
ax.tick_params(
    axis="y",
    direction="in",
    length=6,
    width=1,
    colors="black",
    pad=SPACING["ytick_pad"],
    left=True,
    right=False,
)

# 创建右侧y轴
ax2 = ax.secondary_yaxis("right")
ax2.set_yticks(original_positions)
ax2.set_yticklabels([])
ax2.tick_params(
    axis="y",
    direction="in",
    length=6,
    width=1,
    colors="black",
    pad=SPACING["ytick_pad"],
    left=False,
    right=True,
)

# 设置图形边框
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor("black")
    spine.set_linewidth(1)

# 设置日期刻度
date_positions = np.linspace(0, len(df_interp) - 1, DATE_TICKS, dtype=int)
date_labels = [df_interp.index[i].strftime("%y/%m/%d") for i in date_positions]
ax.set_xticks(date_positions)
ax.set_xticklabels(date_labels, rotation=0, ha="center", fontsize=12)

# 设置刻度间距
ax.tick_params(axis="x", pad=SPACING["xtick_pad"])
ax.tick_params(axis="y", pad=SPACING["ytick_pad"])

# 设置颜色条样式
cbar = ax.collections[0].colorbar
cbar.outline.set_edgecolor("black")
cbar.outline.set_linewidth(1)
cbar.ax.tick_params(labelsize=12, pad=SPACING["cbar_tick_pad"])
cbar.ax.yaxis.label.set_fontsize(13)
cbar.ax.yaxis.labelpad = SPACING["cbar_label_pad"]

zero_pos = (0 - cbar.vmin) / (cbar.vmax - cbar.vmin)
cbar.ax.yaxis.set_major_locator(MultipleLocator(TICK_STEP))
cbar.ax.yaxis.set_minor_locator(MultipleLocator(TICK_STEP / 3))  # 添加次刻度


# 优化布局
plt.tight_layout()
plt.subplots_adjust(top=0.954, bottom=0.114, left=0.116, right=1)

plt.show()
