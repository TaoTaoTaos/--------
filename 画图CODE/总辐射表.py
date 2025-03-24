# -*- coding: utf-8 -*-
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.dates as mdates
from matplotlib.ticker import MultipleLocator

# ================= 全局配置 =================
plt.rcParams.update(
    {
        "font.family": "Microsoft YaHei",
        "font.size": 13,
        "axes.unicode_minus": False,
        "figure.autolayout": True,
    }
)

# ================= 参数设置 =================
DATA_FILE = r"S:\STU-DATA\兴凯湖实地数据\2025.1.18-2.16\锦州阳光数据\输出-锦州阳光数据\锦州阳光每分钟数据\锦州阳光_总辐射相关_全30日数据(每分钟).xlsx"

COLUMN_SETTINGS = {
    "时间 ()": "时间",
    "总辐射1瞬时 (W/㎡)": "辐射1",
    "总辐射2瞬时 (W/㎡)": "辐射2",
}

STYLE_CONFIG = {
    "colors": ["#E63946", "#1D3557"],
    "linewidth": 0.8,
    "date_range": {
        "start": "2025-01-18 00:00:00",
        "end": "2025-02-17 00:00:00",
    },
}


# ================= 数据预处理 =================
def load_and_process(filepath):
    # 读取Excel文件
    df = pd.read_excel(filepath)
    # 重命名列名
    df = df.rename(columns=COLUMN_SETTINGS)
    # 将时间列转换为datetime类型
    df["时间"] = pd.to_datetime(df["时间"], format="%Y/%m/%d %H:%M:%S")
    # 设置时间列为索引
    df = df.set_index("时间").sort_index()
    # 返回指定时间范围内的数据
    return df.loc[
        pd.Timestamp(STYLE_CONFIG["date_range"]["start"]) : pd.Timestamp(
            STYLE_CONFIG["date_range"]["end"]
        )
    ]


# ================= 可视化引擎 =================
def create_visualization(df):
    # 创建包含两个子图的画布
    fig, (ax1, ax2) = plt.subplots(
        2, 1, figsize=(24, 14), sharex=True
    )  # 适当增加画布高度

    # 设置总标题
    fig.suptitle(
        "总辐射瞬时强度",
        fontsize=18,
        fontweight="bold",
        color="#2a2a2a",
    )

    # 绘制第一个子图（辐射1）
    sns.lineplot(
        data=df["辐射1"],
        color=STYLE_CONFIG["colors"][0],
        linewidth=STYLE_CONFIG["linewidth"],
        alpha=0.85,
        ax=ax1,
    )

    # 绘制第二个子图（辐射2）
    sns.lineplot(
        data=df["辐射2"],
        color=STYLE_CONFIG["colors"][1],
        linewidth=STYLE_CONFIG["linewidth"],
        alpha=0.85,
        ax=ax2,
    )

    # ================= 公共配置函数 =================
    def configure_axes(ax):
        # 设置x轴主刻度间隔为1天
        ax.xaxis.set_major_locator(mdates.DayLocator(interval=5))
        # 设置x轴主刻度格式为月/日
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%m/%d"))
        # 设置x轴次刻度间隔为6、12、18小时
        ax.xaxis.set_minor_locator(mdates.HourLocator(byhour=[6, 12, 18]))
        # 设置x轴刻度标签旋转角度
        ax.tick_params(axis="x", rotation=35, labelsize=12, pad=12)
        # 设置y轴主刻度间隔为100
        ax.yaxis.set_major_locator(MultipleLocator(100))
        # 设置y轴次刻度间隔为20
        ax.yaxis.set_minor_locator(MultipleLocator(20))
        # 设置x轴主刻度线样式
        ax.grid(True, which="major", axis="x", linestyle="--", linewidth=0.8, alpha=0.6)
        # 设置x轴次刻度线样式
        ax.grid(True, which="minor", axis="x", linestyle=":", linewidth=0.5, alpha=0.3)
        # 设置y轴主刻度线样式
        ax.grid(True, which="major", axis="y", linestyle="--", linewidth=0.8, alpha=0.5)

        # 设置边框颜色和宽度
        for spine in ax.spines.values():
            spine.set_color("gray")
            spine.set_linewidth(1)

        # 强制设置时间范围
        ax.set_xlim(
            pd.Timestamp(STYLE_CONFIG["date_range"]["start"]),
            pd.Timestamp(STYLE_CONFIG["date_range"]["end"]),
        )

    # 配置第一个子图
    configure_axes(ax1)
    ax1.set_ylim(-20, 500)  # 调整Y轴范围
    ax1.set_ylabel("下行瞬时总辐射 (W/㎡)", fontsize=14, labelpad=18)

    # 配置第二个子图
    configure_axes(ax2)
    ax2.set_ylim(-20, 750)
    ax2.set_ylabel("上行瞬时总辐射 (W/㎡)", fontsize=14, labelpad=18)

    # ================= 背景色配置 =================
    def add_daylight(ax):
        for day in pd.date_range(
            start=STYLE_CONFIG["date_range"]["start"],
            end=STYLE_CONFIG["date_range"]["end"],
        ):
            ax.axvspan(
                day + pd.Timedelta(hours=6),
                day + pd.Timedelta(hours=18),
                facecolor="gold",
                alpha=0.06,
                zorder=0,
            )

    add_daylight(ax1)
    add_daylight(ax2)

    # 调整子图间距
    plt.subplots_adjust(hspace=0.08)

    plt.show()


# ================= 执行主程序 =================
if __name__ == "__main__":
    df_processed = load_and_process(DATA_FILE)
    create_visualization(df_processed)
    print("可视化完成，请查看弹出的窗口。")
