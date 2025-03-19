import os
import pandas as pd
from pathlib import Path


def process_daily_average(input_folder, output_folder):
    # 创建输出文件夹
    output_path = Path(input_folder) / output_folder
    output_path.mkdir(exist_ok=True)

    # 遍历输入文件夹中的所有xlsx文件
    for file in Path(input_folder).glob("*.xlsx"):
        if "(每分钟)" not in file.name:
            continue
        print(file.name)

        # 读取Excel文件
        df = pd.read_excel(file)

        # 转换时间列为datetime类型
        df["时间"] = pd.to_datetime(df["时间"])

        # 提取日期列
        df["日期"] = df["时间"].dt.date
        print("计算中...")
        # 按日期分组计算平均值
        daily_avg = df.groupby("日期").mean(numeric_only=True).reset_index()

        # 构建输出文件名
        new_name = file.name.replace("(每分钟)", "(每日)")
        output_file = output_path / new_name

        # 保存结果
        daily_avg.to_excel(output_file, index=False)
        print(f"已生成：{output_file}")

    print("处理完成！")
    print(f"输出文件夹路径：{output_path}")


if __name__ == "__main__":
    input_folder = (
        r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x初始数据\CR100X处理后数据"
    )
    output_folder = "CR1000X逐日数据"

    process_daily_average(input_folder, output_folder)
