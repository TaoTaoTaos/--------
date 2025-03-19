import pandas as pd
import os

# 定义文件夹路径和输出文件夹
input_directory = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据"
output_directory = (
    r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据\输出-锦州阳光数据"
)

# 确保输出文件夹存在，如果不存在则创建
os.makedirs(output_directory, exist_ok=True)

# 定义输出文件名
output_file = os.path.join(output_directory, "锦州阳光_电量_全30日数据(每分钟).xlsx")

# 定义要提取的列名
columns_to_extract = [
    "时间 ()",
    "电量 (V)",
]

# ========================================================
# 创建一个空的 DataFrame 用于存储合并的数据
merged_data = pd.DataFrame()

# 遍历目录下的所有 Excel 文件
for file in os.listdir(input_directory):
    if file.endswith(".xls"):  # 确保是 Excel 文件
        print(file)
        file_path = os.path.join(input_directory, file)  # 构建完整的文件路径

        # 读取 Excel 文件
        try:
            data = pd.read_excel(file_path)
            # 提取指定的列

            extracted_data = data[columns_to_extract]
            # 将提取的数据添加到合并 DataFrame
            merged_data = pd.concat([merged_data, extracted_data], ignore_index=True)
        except Exception as e:
            print(f"读取文件 {file} 时发生错误: {e}")

# 将合并后的数据输出到新的 Excel 文件
print("正在合并...")
merged_data.to_excel(output_file, index=False)

print(f"数据已成功合并并输出到 {output_file}")
