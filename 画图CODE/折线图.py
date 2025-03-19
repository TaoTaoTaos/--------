import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# 文件路径（使用原始字符串避免转义问题）
file_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x初始数据\CR100X处理后数据\CR1000X平均数据(每分钟).xlsx"
plt.rcParams["font.family"] = "sans-serif"
plt.rcParams["font.sans-serif"] = ["Microsoft YaHei"]

# 读取Excel数据
try:
    df = pd.read_excel(file_path, engine="openpyxl")
except FileNotFoundError:
    print("文件路径错误，请确认文件是否存在！")
    exit()

# 定义物理范围常量
PHYSICAL_MIN = 0  # 冰厚最小值（单位：米）
PHYSICAL_MAX = 0.4  # 冰厚最大值（单位：米）

# 确认列名（根据实际数据调整）
ice_thickness_col = "高度计（冰厚）"  # 冰厚数据列名
time_col = "时间"  # 时间列名

# 检查列是否存在
if ice_thickness_col not in df.columns or time_col not in df.columns:
    print("列名不匹配，请检查数据列名！")
    print("可用列名：", df.columns.tolist())
    exit()

# 过滤极端值：将超出范围的值设为NaN
df[ice_thickness_col] = df[ice_thickness_col].where(
    (df[ice_thickness_col] >= PHYSICAL_MIN) & (df[ice_thickness_col] <= PHYSICAL_MAX),
    np.nan,
)

# 转换时间列为datetime格式
df[time_col] = pd.to_datetime(df[time_col], errors="coerce")

# 绘制折线图
plt.figure(figsize=(15, 6))
plt.plot(
    df[time_col], df[ice_thickness_col], linestyle="-", linewidth=1, color="#1f77b4"
)
plt.title("兴凯湖冰厚随时间变化趋势（过滤极端值后）", fontsize=14)
plt.xlabel("时间", fontsize=12)
plt.ylabel("冰厚（米）", fontsize=12)
plt.grid(True, linestyle="--", alpha=0.7)
plt.xticks(rotation=45)
plt.tight_layout()  # 自动调整布局

plt.show()
