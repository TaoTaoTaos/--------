import pandas as pd
from datetime import timedelta


def check_time_continuity():
    # 文件路径配置
    file_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据\输出-锦州阳光数据\锦州阳光每分钟数据\锦州阳光_温度1-9_全30日数据(每分钟).xlsx"
    output_file_path = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据\输出-锦州阳光数据\锦州阳光每分钟数据\缺失时间段统计.txt"

    try:
        # 读取Excel文件的第一列（时间列）
        df = pd.read_excel(
            file_path,
            usecols=[0],  # 读取第一列
            header=0,  # 无表头
            names=["时间"],  # 列名设为"时间"
        )
        print("✅ 文件读取成功")
    except Exception as e:
        print(f"❌ 文件读取失败：\n{str(e)}")
        print("请检查：1. 文件路径是否正确 2. 文件是否被占用 3. 文件格式是否为xlsx")
        return

    # 打印前5行数据，检查是否正确读取
    print("\n前5行数据：")
    print(df.head())

    # 检查时间列是否存在空值
    if df["时间"].isnull().any():
        print("❌ 时间列中存在空值，请检查数据源")
        invalid_rows = df[df["时间"].isnull()]
        print("前5条无效数据位置（行号从1开始）：")
        print(invalid_rows.index[:5].values + 1)
        return

    # 时间格式转换
    try:
        # 将时间列转换为 datetime 格式
        df["时间"] = pd.to_datetime(df["时间"], infer_datetime_format=True)
        # 忽略秒部分，将时间截断到分钟级别
        df["时间"] = df["时间"].dt.floor("T")  # "T" 表示分钟
        print("\n✅ 时间格式转换成功，并已忽略秒部分")
    except Exception as e:
        print(f"❌ 时间格式转换失败：\n{str(e)}")
        return

    # 按时间排序并去重
    df = df.sort_values("时间").drop_duplicates()

    # 生成完整时间序列（分钟级别）
    start_time = df["时间"].iloc[0]
    end_time = df["时间"].iloc[-1]
    full_range = pd.date_range(start=start_time, end=end_time, freq="T")

    # 找出缺失时间点
    missing = full_range[~full_range.isin(df["时间"])]

    # 结果输出
    if len(missing) == 0:
        print("\n✅ 时间序列完整，无缺失数据")
        print(f"时间范围：{start_time} 至 {end_time}")
        print(f"总数据量：{len(df)}条")
        return

    # 分组显示连续缺失时间段
    print(f"\n⚠️ 发现{len(missing)}个缺失时间点")
    print("----------------------------------------")

    missing_series = pd.Series(missing, name="缺失时间")
    gaps = missing_series.groupby(
        (missing_series.diff() != timedelta(minutes=1)).cumsum()
    )

    # 统计缺失时间段的信息
    gap_info = []
    for gap_id, (_, gap) in enumerate(gaps, 1):
        if len(gap) == 1:
            gap_info.append(
                {
                    "类型": "单点缺失",
                    "开始时间": gap.iloc[0],
                    "结束时间": gap.iloc[0],
                    "持续时长": 1,
                }
            )
            print(f"缺失时间点 #{gap_id}: {gap.iloc[0].strftime('%Y-%m-%d %H:%M')}")
        else:
            duration = (gap.iloc[-1] - gap.iloc[0]).total_seconds() / 60 + 1
            gap_info.append(
                {
                    "类型": "连续缺失",
                    "开始时间": gap.iloc[0],
                    "结束时间": gap.iloc[-1],
                    "持续时长": int(duration),
                }
            )
            print(f"连续缺失时间段 #{gap_id}:")
            print(f"▸ 开始时间：{gap.iloc[0].strftime('%Y-%m-%d %H:%M')}")
            print(f"▸ 结束时间：{gap.iloc[-1].strftime('%Y-%m-%d %H:%M')}")
            print(f"▸ 持续时长：{int(duration)}分钟")
            print(
                f"▸ 缺失时间点示例：{gap.iloc[0].strftime('%H:%M')} ~ {gap.iloc[-1].strftime('%H:%M')}"
            )
        print("----------------------------------------")

    # 将统计信息写入TXT文件
    with open(output_file_path, "w", encoding="utf-8") as f:
        f.write("====== 缺失时间段统计 ======\n")
        f.write(f"时间范围：{start_time} 至 {end_time}\n")
        f.write(f"应存在数据：{len(full_range)}条\n")
        f.write(f"实际存在数据：{len(df)}条\n")
        f.write(f"完整度：{len(df)/len(full_range):.2%}\n\n")

        f.write("====== 缺失时间段详情 ======\n")
        for info in gap_info:
            if info["类型"] == "单点缺失":
                f.write(f"单点缺失：{info['开始时间'].strftime('%Y-%m-%d %H:%M')}\n")
            else:
                f.write(
                    f"连续缺失：{info['开始时间'].strftime('%Y-%m-%d %H:%M')} ~ "
                    f"{info['结束时间'].strftime('%Y-%m-%d %H:%M')}, "
                    f"持续时长：{info['持续时长']}分钟\n"
                )

        # 统计缺失时间段的汇总信息
        f.write("\n====== 缺失时间段汇总 ======\n")
        f.write(f"总缺失时间点数量：{len(missing)}\n")
        f.write(f"总缺失时间段数量：{len(gap_info)}\n")
        if len(gap_info) > 0:
            max_gap = max(gap_info, key=lambda x: x["持续时长"])
            min_gap = min(gap_info, key=lambda x: x["持续时长"])
            f.write(
                f"最长缺失时间段：{max_gap['持续时长']}分钟（{max_gap['开始时间'].strftime('%Y-%m-%d %H:%M')} ~ {max_gap['结束时间'].strftime('%Y-%m-%d %H:%M')})\n"
            )
            f.write(
                f"最短缺失时间段：{min_gap['持续时长']}分钟（{min_gap['开始时间'].strftime('%Y-%m-%d %H:%M')} ~ {min_gap['结束时间'].strftime('%Y-%m-%d %H:%M')})\n"
            )

    print(f"\n📊 统计信息和缺失时间段已保存到：{output_file_path}")


if __name__ == "__main__":
    print("====== 时间序列完整性检查程序 ======")
    check_time_continuity()
    print("\n检测完成，请关闭窗口")
