from matplotlib import font_manager

# 获取所有系统字体名称（去重）
font_names = {f.name for f in font_manager.fontManager.ttflist}

# 打印所有字体名称（按字母顺序）
print("系统中安装的字体列表（按字母顺序排序）：")
for name in sorted(font_names):
    print(f" - {name}")

# 检查中文字体是否存在
print("\n常见中文字体检测:")
for font in ["SimHei", "Microsoft YaHei", "KaiTi", "FangSong", "STSong"]:
    if font in font_names:
        print(f"✅ 找到中文字体: {font}")
    else:
        print(f"❌ 缺失中文字体: {font}")
