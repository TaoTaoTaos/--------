import pandas as pd
import os
from datetime import timedelta


def process_all_files():
    # 配置路径
    input_dir = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据\输出-锦州阳光数据\锦州阳光每分钟数据"
    output_dir = os.path.join(input_dir, "补全数据")
    log_file = os.path.join(output_dir, "数据处理日志.txt")

    # 创建输出目录
    os.makedirs(output_dir, exist_ok=True)

    # 获取所有Excel文件
    excel_files = [
        f
        for f in os.listdir(input_dir)
        if f.endswith(".xlsx") and not f.startswith("~$")
    ]

    if not excel_files:
        print("输入目录中没有Excel文件")
        return

    # 初始化日志
    log_content = [
        "====== 数据处理日志 ======",
        f"输入目录：{input_dir}",
        f"输出目录：{output_dir}",
        f"共发现{len(excel_files)}个Excel文件需要处理",
        "=" * 30,
    ]

    processed_files = []

    for file_name in excel_files:
        file_path = os.path.join(input_dir, file_name)
        base_name = os.path.basename(file_path)
        log_content.append(f"\n处理文件：{base_name}")

        try:
            # 读取Excel文件
            df = pd.read_excel(file_path, header=0)
            original_time_col = df.columns[0]
            df = df.rename(columns={original_time_col: "时间"})

            # 处理空值
            if df["时间"].isnull().any():
                df = df.dropna(subset=["时间"])
                log_content.append("⚠️ 时间列存在空值，已删除对应行")

            # 时间格式处理
            df["时间"] = pd.to_datetime(df["时间"]).dt.floor("T")
            df = df.sort_values("时间").drop_duplicates(subset=["时间"], keep="first")

            # 生成完整时间序列
            start_time = df["时间"].min()
            end_time = df["时间"].max()
            full_range = pd.date_range(start=start_time, end=end_time, freq="T")

            # 重新索引并插值
            df_full = (
                df.set_index("时间")
                .reindex(full_range)
                .interpolate(method="time")
                .reset_index()
                .rename(columns={"index": "时间"})
            )

            # 恢复原始列名
            df_full = df_full.rename(columns={"时间": original_time_col})

            # 保存文件
            output_name = f"{os.path.splitext(file_name)[0]}_补全.xlsx"
            output_path = os.path.join(output_dir, output_name)
            df_full.to_excel(output_path, index=False)
            processed_files.append(output_path)

            # 记录日志
            log_content.extend(
                [
                    f"✅ 处理成功",
                    f"时间范围：{start_time} 至 {end_time}",
                    f"原数据量：{len(df)}条",
                    f"补全后数据量：{len(df_full)}条",
                    f"补全缺失点：{len(df_full)-len(df)}处",
                    f"保存路径：{output_path}",
                ]
            )

        except Exception as e:
            log_content.append(f"❌ 处理失败：{str(e)}")
            continue

    # 写入日志文件
    with open(log_file, "w", encoding="utf-8") as f:
        f.write("\n".join(log_content))

    # 打印结果
    print("\n".join(log_content))
    print("\n====== 处理完成 ======")
    print(f"处理文件总数：{len(excel_files)}")
    print(f"成功处理文件：{len(processed_files)}")
    print(f"生成文件列表：")
    for path in processed_files:
        print(f"▸ {path}")


if __name__ == "__main__":
    print("====== 时间序列补全程序 ======")
    process_all_files()
    print("\n程序执行完毕，请关闭窗口")
