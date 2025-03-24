import pandas as pd
import os

# 文件路径配置（注意：路径中的反斜杠需要转义或使用原始字符串）
input_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x数据\CR1000X处理后数据\日均值数据.csv"
output_dir = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\cr1000x数据\CR1000X处理后数据"
output_filename = "计算得出冰厚.csv"
output_path = os.path.join(output_dir, output_filename)


def calculate_ice_thickness():
    try:
        # 检查输入文件是否存在
        if not os.path.exists(input_path):
            raise FileNotFoundError(f"输入文件未找到: {input_path}")

        # 读取CSV文件（尝试常见中文编码）
        try:
            df = pd.read_csv(input_path, encoding="utf-8")
        except UnicodeDecodeError:
            df = pd.read_csv(input_path, encoding="gbk")

        # 检查数据列是否存在
        if "高度计" not in df.columns:
            raise ValueError("CSV文件中缺少'高度计'列，请检查数据格式")

        # 初始冰厚（单位：米）
        initial_thickness = 0.62  # 对应62厘米
        ice_thickness = [initial_thickness]

        # 逐日计算冰厚
        for i in range(1, len(df)):
            delta = df["高度计"].iloc[i] - df["高度计"].iloc[i - 1]
            new_thickness = ice_thickness[-1] - delta
            ice_thickness.append(round(new_thickness, 6))  # 保留6位小数

        # 添加结果列
        df["冰厚(m)"] = ice_thickness
        df["冰厚(cm)"] = [round(t * 100, 2) for t in ice_thickness]  # 增加厘米列

        # 创建输出目录（如果不存在）
        os.makedirs(output_dir, exist_ok=True)

        # 保存结果（使用与输入相同的编码）
        df.to_csv(output_path, index=False, encoding="gbk")
        print(f"计算完成！结果已保存至:\n{output_path}")
        print("\n前5行结果预览:")
        print(df.head())

    except Exception as e:
        print(f"错误发生: {str(e)}")
        print("建议检查:")
        print("1. 文件路径是否存在")
        print('2. CSV文件是否包含"时间"和"高度计"列')
        print("3. 文件编码是否为GBK/UTF-8")


if __name__ == "__main__":
    calculate_ice_thickness()
