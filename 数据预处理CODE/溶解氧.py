import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib import font_manager
from matplotlib.colors import LinearSegmentedColormap

# ================= 参数配置区域（用户可修改） =================
SELECTED_COLS = [
    "溶解氧1（计算值）",
    "溶解氧2（计算值）",
]
DEPTHS = [-0.7, -2.1]  # 单位：米 (80cm~200cm)
VMIN = 30
VMAX = -10
DATE_TICKS = 10
COLORS = ["#003d8c", "#00c4b3"]  # 暗海军蓝 - 孔雀石绿
# ===========================================================

# 设置中文字体
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["SimHei"]
plt.rcParams["axes.unicode_minus"] = False

# 验证字体可用性
if "Microsoft YaHei" not in font_manager.findSystemFonts():
    print("警告：Microsoft YaHei字体未找到，尝试使用SimHei")

# 读取数据（注意路径验证）
try:
    data_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x初始数据\CR100X处理后数据\CR1000X平均数据(每分钟).xlsx"
    df = pd.read_excel(data_path)
except FileNotFoundError:
    print(f"错误：文件未找到，请检查路径是否正确：{data_path}")
    exit()

# 时间序列处理
df["时间"] = pd.to_datetime(df["时间"])
df.set_index("时间", inplace=True)

# 数据列选择与深度对应
assert len(SELECTED_COLS) == len(DEPTHS), "SELECTED_COLS和DEPTHS长度必须相同"
df_temp = df[SELECTED_COLS].copy()
df_temp.columns = [f"{abs(d)*100:.0f}cm" for d in DEPTHS]

# 创建自定义颜色映射
cmap_custom = LinearSegmentedColormap.from_list("红蓝渐变", COLORS)

# 绘制热力图
plt.figure(figsize=(17, 9))
ax = sns.heatmap(
    df_temp.T,
    cmap=cmap_custom,
    cbar_kws={
        "label": "溶解氧",
        "shrink": 0.8,
        "aspect": 20,
        "pad": 0.03,  # 减小颜色条与主图的间距
    },
    vmin=VMIN,
    vmax=VMAX,
    yticklabels=1,
    xticklabels=False,
)

# 设置坐标轴样式
ax.set_yticks(np.arange(len(DEPTHS)) + 0.5)
ax.set_yticklabels([f"{int(abs(d)*100)}cm" for d in DEPTHS], fontsize=12)
ax.set_xlabel("日期", fontsize=12)
ax.set_ylabel("深度 (cm)", fontsize=12)

# 设置日期刻度
date_positions = np.linspace(0, len(df_temp) - 1, DATE_TICKS, dtype=int)
date_labels = [df_temp.index[i].strftime("%m-%d") for i in date_positions]
ax.set_xticks(date_positions)
ax.set_xticklabels(date_labels, rotation=45, ha="right", fontsize=12)

# 设置图形边框
for spine in ax.spines.values():
    spine.set_visible(True)
    spine.set_edgecolor("black")
    spine.set_linewidth(1)

# 设置颜色条样式
cbar = ax.collections[0].colorbar
cbar.outline.set_edgecolor("black")
cbar.outline.set_linewidth(1)
cbar.ax.tick_params(labelsize=12)
cbar.ax.yaxis.label.set_fontsize(12)

# 优化布局（关键调整）
plt.tight_layout()
plt.subplots_adjust(
    left=0.08, right=0.92  # 减小左侧空白  # 减小右侧空白，使左右边距对称
)

plt.show()
