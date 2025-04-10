library(tidyverse)
library(readxl)
library(scales)
library(lubridate)
library(splines)
library(viridis)

# ================= 修正后的参数配置区域 =================
SELECTED_COLS <- c(
  "CR温度1", "CR温度2", "温度9 (℃)", "温度8 (℃)", 
  "温度7 (℃)", "温度6 (℃)", "温度5 (℃)", 
  "温度4 (℃)", "温度3 (℃)", "温度2 (℃)", "温度1 (℃)"
)

# 修正深度定义（单位：米）
DEPTHS <- c(0, -0.2, -0.4, -0.6, -0.8, -1, -1.2, -1.4, -1.6, -1.8, -2)  # 正确闭合数组

# 单独定义其他参数
INTERP_DEPTH_STEP <- 0.001  # 插值步长 (米)
VMIN <- -18
VMAX <- 5
TICK_STEP <- 3  # 颜色条主刻度间隔 (℃)
DATE_TICKS <- 5  # 日期刻度数量

COLORS <- c("#FF0000", "#FFFF00", "#5deb69", "#00FFFF", "#0000FF")
COLOR_VALUES <- c(-18, -12, -6, 0, 5)

SPACING <- list(
  xlabel_pad = 15,
  ylabel_pad = 20,
  xtick_pad = 10,
  ytick_pad = 8,
  cbar_label_pad = 15,
  cbar_tick_pad = 8
)
# =======================================================

# 确保加载所需包
library(circlize)  # 添加colorRamp2函数所需的包
            
            # ================= 数据准备 =================
            # 读取数据并预处理
            df <- read_excel("your_data_path.xlsx") %>%
              mutate(时间 = as.POSIXct(时间)) %>%
              arrange(时间) %>%
              column_to_rownames("时间") %>%
              select(all_of(SELECTED_COLS)) %>%
              mutate(across(everything(), as.numeric))
            
            # ================= 插值处理 =================
            new_depths <- seq(0, -2, by = -INTERP_DEPTH_STEP)
            interp_fn <- function(row) {
              spline(
                x = sort(DEPTHS),
                y = rev(row),
                xout = new_depths,
                method = "natural"
              )$y
            }
            
            df_interp <- df %>%
              apply(1, interp_fn) %>%
              t() %>%
              as.data.frame() %>%
              set_names(sprintf("%dcm", abs(new_depths)*100)) %>%
              rownames_to_column("time") %>%
              mutate(time = as.POSIXct(time)) %>%
              pivot_longer(-time, names_to = "depth", = "temp") %>%
              mutate(
                depth = factor(depth, levels = unique(depth)),
                depth_num = as.numeric(gsub("cm", "", depth))
              )
            
            # ================= 可视化 =================
            # 创建自定义颜色梯度
            color_ramp <- colorRamp2(
              breaks = (COLOR_VALUES - VMIN)/(VMAX - VMIN),
              colors = COLORS
            )
            
            # 生成日期刻度
            date_breaks <- df_interp %>%
              pull(time) %>%
              unique() %>%
              as.POSIXct() %>%
              seq(length.out = DATE_TICKS)
            
            ggplot(df_interp, aes(x = time, y = reorder(depth, depth_num), fill = temp)) +
              geom_tile() +
              scale_fill_gradientn(
                colours = color_ramp(seq(0, 1, length.out = 256)),
                limits = c(VMINMAX),
                breaks = seq(VMIN, VMAX, TICK_STEP),
                guide = guide_colorbar(
                  title = "温度 (℃)",
                  title.position = "top",
                  barheight = unit(0.8, "npc"),
                  label.position = "right"
                )
              ) +
              scale_x_datetime(
                breaks = date_breaks,
                labels = date_format("%y/%m/%d"),
                expand = expansion(0)
              ) +
              scale_y_discrete(
                breaks = sprintf("%dcm", abs(DEPTHS)*100),
                position = "right",
                expand = expansion(0)
              ) +
              labs(x = "日期", y = "深度 (cm)") +
              theme_minimal(base_size = 12) +
              theme(
                axis.title.x = element_text(margin = margin(t = SPACING$xlabel_pad)),
                axis.title.y = element_text(margin = margin(r = SPACING$ylabel_pad)),
                axis.text.x = element_text(angle = 0, margin = margin(t = SPACING$xtick_pad)),
                axis.text.y = element_text(margin = margin(r = SPACING$ytick_pad)),
                legend.title = element_text(margin = margin(b = SPACING$cbar_label_pad)),
                legend.text = element_text(margin = margin(r = SPACING$cbar_tick_pad)),
                panel.grid = element_blank(),
                panel.border = element_rect(fill = NA, color = "black", linewidth = 1),
                plot.margin = margin(1, 1, 1, 1, "cm")
              )
            
            # ================= 保存图像 =================
            ggsave("temperature_heatmap.png", width = 17, height = 9, dpi = 300, units = "in")