import geopandas as gpd
import pandas as pd

# 读取原始 Shapefile
shp_path = r"S:\STU-DATA\兴凯湖实地数据\野外数据\兴凯湖采样点\兴凯湖采样点.shp"
gdf = gpd.read_file(shp_path)

# 定义冰厚数据（仅样点编号和冰厚）
ice_data = {
    "样点编": [
        "XKH14",
        "XKH01",
        "XKH12",
        "XKH13",
        "XKH08",
        "XKH10",
        "XKH16",
        "XKH05",
        "XXK17",
        "XXK01",
        "XXK02",
    ],
    "冰厚": [
        625.1,
        625.6,
        615.3,
        614.2,
        592.4,
        665.8,
        657.1,
        655.6,
        675.6,
        621.4,
        659.9,
    ],
}

# 转换为 DataFrame
ice_df = pd.DataFrame(ice_data)

# 合并到原始地理数据（仅添加冰厚字段）
gdf = gdf.merge(ice_df, on="样点编", how="left")

# 保存为新 Shapefile（保留原始所有字段，仅新增冰厚）
output_path = (
    r"S:\STU-DATA\兴凯湖实地数据\野外数据\兴凯湖采样点\兴凯湖采样点_仅冰厚.shp"
)
gdf.to_file(output_path, encoding="utf-8")

print(f"冰厚字段已添加！结果保存至 {output_path}")
