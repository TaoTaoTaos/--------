import pandas as pd

# 读取 Excel 文件中的 Sheet1 和 Sheet2
file_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x初始数据\cr1000x有用的原始数据.xls"
sheet1 = pd.read_excel(file_path, sheet_name="Sheet1")
sheet2 = pd.read_excel(file_path, sheet_name="Sheet2")

# 合并两张表
data = pd.concat([sheet1, sheet2], ignore_index=True)

# 将时间列转为 datetime 类型并设置为索引
data["时间"] = pd.to_datetime(data["时间"])
data.set_index("时间", inplace=True)

# 计算平均值，使用 'min' 代替 'T'
mean_data = data.resample("min").mean()  # 'min'表示按分钟重采样

# 重置索引以保留时间列
mean_data.reset_index(inplace=True)

# 格式化时间
mean_data["时间"] = mean_data["时间"].dt.strftime("%Y/%m/%d %H:%M:%S")

# 保存到新的 Excel 文件
output_file_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x初始数据\CR1000X平均数据(每分钟).xlsx"
mean_data.to_excel(output_file_path, index=False)

print(f"数据平均值已保存至：{output_file_path}")
