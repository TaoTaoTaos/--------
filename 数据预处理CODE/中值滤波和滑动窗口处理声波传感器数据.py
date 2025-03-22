import pandas as pd
import numpy as np
import os
from datetime import datetime

# ================== 用户可调参数 ==================
input_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x数据\CR1000X处理后数据\CR1000X平均数据(每分钟).xlsx"  # 输入文件路径
output_dir = r"S:\STU-DATA\兴凯湖实地数据\处理结果\每日冰厚结果"  # 输出文件夹路径

median_window_global = 61  # 全局中值滤波窗口（单位：分钟，建议1小时以上）
median_window_local = 3  # 局部中值滤波窗口（单位：分钟）
smooth_window = 5  # 滑动平均窗口
# ================================================

# 创建输出文件夹（如果不存在）
os.makedirs(output_dir, exist_ok=True)


def process_ice_thickness():
    """主处理函数：读取数据、滤波、计算日均冰厚"""
    # 读取原始数据
    try:
        df = pd.read_excel(input_path, engine="openpyxl")  # 确保安装openpyxl
        df["时间"] = pd.to_datetime(df["时间"])
        df.set_index("时间", inplace=True)
        print("数据读取成功，时间范围:", df.index.min(), "至", df.index.max())
    except Exception as e:
        print("文件读取失败，请检查路径和文件格式:", str(e))
        return

    # 按天分组处理
    daily_groups = df.groupby(pd.Grouper(freq="D"))
    results = []

    for day, day_data in daily_groups:
        # 提取当天数据并去空
        ice_series = day_data["高度计（冰厚）"].dropna()
        if len(ice_series) < 10:  # 忽略数据量不足的天
            print(f"跳过 {day.date()}（数据量不足）")
            continue

        # 分阶段滤波处理
        try:
            # 第一阶段：全局中值滤波（去除全天异常段）
            ice_global = ice_series.rolling(
                window=median_window_global, min_periods=1, center=True
            ).median()

            # 第二阶段：局部中值滤波（细化处理）
            ice_local = ice_global.rolling(
                window=median_window_local, min_periods=1, center=True
            ).median()

            # 滑动平均平滑
            ice_smoothed = ice_local.rolling(
                window=smooth_window, min_periods=1, center=True
            ).mean()

            # 计算当日均值
            daily_mean = np.round(ice_smoothed.mean(), 3)
            results.append(
                {
                    "日期": day.date(),
                    "日均冰厚(m)": daily_mean,
                    "数据点数": len(ice_series),
                }
            )
            print(f"已处理 {day.date()}，冰厚: {daily_mean}m")
        except Exception as e:
            print(f"处理 {day.date()} 时出错:", str(e))

    # 保存结果到Excel
    if results:
        result_df = pd.DataFrame(results)
        output_path = os.path.join(output_dir, "兴凯湖每日冰厚均值_处理结果.xlsx")
        result_df.to_excel(output_path, index=False)
        print(f"\n处理完成！结果已保存至: {output_path}")
        print("统计摘要:\n", result_df.describe())
    else:
        print("未生成有效结果，请检查输入数据")


if __name__ == "__main__":
    process_ice_thickness()
