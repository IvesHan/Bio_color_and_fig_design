import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd
from io import BytesIO
import os
# 确保 utils.py 和 requirements.txt 已经就绪
try:
    from utils import simulate_colorblindness, convert_dpi
except ImportError:
    st.error("⚠️ 缺少 utils.py 文件。请确保 utils.py 与 app.py 在同一目录下。")

# --- 页面配置 ---
st.set_page_config(page_title="BioMed Design Hub", page_icon="🧬", layout="wide")

# --- 预设数据 (保持不变) ---
CNS_PALETTES = {
    "Nature_Npg": ["#E64B35", "#4DBBD5", "#00A087", "#3C5488", "#F39B7F", "#8491B4", "#91D1C2", "#DC0000"],
    "Science_HighContrast": ["#0C7BDC", "#FFC20A", "#994F00", "#E1BE6A", "#40B0A6", "#1A85FF", "#D41159"],
    "Cell_Pastel": ["#A1C9F4", "#FFB482", "#8DE5A1", "#FF9F9B", "#D0BBFF", "#DEBB9B", "#FAB0E4"],
    "Classic_Dark": ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd", "#8c564b", "#e377c2"],
    "Grayscale_Elegant": ["#252525", "#525252", "#737373", "#969696", "#bdbdbd", "#d9d9d9", "#f0f0f0"]
}

# --- 侧边栏 ---
st.sidebar.title("🧬 BioDesign Hub")
st.sidebar.caption("CNS 级科研绘图辅助工具")
app_mode = st.sidebar.radio("功能导航", [
    "🎨 配色 & 可及性 (Palette)", 
    "🖼️ 矢量素材库 (Assets)", 
    "🛠️ 格式转换工具 (Tools)"
])

# --- 模块 1: 配色 & 可及性 ---
if app_mode == "🎨 配色 & 可及性 (Palette)":
    st.title("🎨 CNS 配色方案与可及性检查")
    
    col_main, col_preview = st.columns([1, 2])
    
    with col_main:
        selected_style = st.selectbox("选择配色风格", list(CNS_PALETTES.keys()))
        colors = CNS_PALETTES[selected_style]
        
        st.markdown("### 👁️ 色盲模拟")
        cb_type = st.selectbox("模拟视觉类型", ["正常视觉", "Deuteranopia (绿盲/最常见)", "Protanopia (红盲)", "Tritanopia (蓝盲)"])
        
        st.markdown("---")
        st.markdown("**色号预览 (Hex):**")
        for c in colors:
            simulated_c = c if cb_type == "正常视觉" else simulate_colorblindness(c, cb_type.split()[0])
            c1, c2 = st.columns([1, 3])
            c1.markdown(f'<div style="background-color:{simulated_c}; height:25px; border-radius:3px; border:1px solid #ddd;"></div>', unsafe_allow_html=True)
            c2.text(f"{c} → {simulated_c}" if cb_type != "正常视觉" else c)

    with col_preview:
        st.subheader("📊 实时效果预览")
        fig, ax = plt.subplots(figsize=(8, 4))
        # 根据选择模拟颜色
        plot_colors = [simulate_colorblindness(c, cb_type.split()[0]) if cb_type != "正常视觉" else c for c in colors]
        
        # 模拟数据
        data = pd.DataFrame({
            "Group": [f"Group {i+1}" for i in range(len(plot_colors[:5]))],
            "Value": np.random.randint(5, 15, size=len(plot_colors[:5]))
        })
        sns.barplot(x="Group", y="Value", data=data, palette=plot_colors, ax=ax, edgecolor=".2")
        sns.despine()
        st.pyplot(fig)
        
        if cb_type != "正常视觉":
            st.info("💡 如果柱状图颜色难以区分，建议在左侧更换配色方案。")

        st.subheader("💻 Matplotlib 代码生成")
        st.markdown("复制下方代码到 Jupyter Notebook：")
        st.code(f"""
import seaborn as sns
import matplotlib.pyplot as plt

# CNS Style: {selected_style}
colors = {colors}
sns.set_palette(sns.color_palette(colors))

# Example Plot
sns.barplot(x=["A", "B", "C"], y=[1, 2, 3])
plt.show()
""", language="python")

# --- 模块 2: 矢量素材库 (已整合外部资源) ---
elif app_mode == "🖼️ 矢量素材库 (Assets)":
    st.title("🖼️ 生物医学矢量素材库")
    
    tab1, tab2 = st.tabs(["📂 本地精选素材", "🌐 外部开源资源站"])

    # --- Tab 1: 本地下载 ---
    with tab1:
        st.markdown("### 精选 SVG 矢量图下载")
        st.caption("以下素材为矢量格式 (SVG)，支持无限放大不失真，可在 AI/Inkscape 中二次编辑。")
        
        if not os.path.exists("assets/vectors"):
            st.warning("⚠️ 未检测到本地素材库。请运行 `init_assets.py` 脚本进行初始化。")
        else:
            files = [f for f in os.listdir("assets/vectors") if f.endswith(".svg")]
            if not files:
                st.info("本地库暂无文件。")
            
            # 使用 Grid 布局展示
            for i in range(0, len(files), 3):
                cols = st.columns(3)
                for j in range(3):
                    if i + j < len(files):
                        file_name = files[i + j]
                        with cols[j]:
                            # 卡片式布局
                            with st.container(border=True):
                                st.markdown(f"**{file_name.replace('.svg', '').replace('_', ' ').title()}**")
                                st.image("https://placehold.co/150x100?text=SVG+Preview", caption="矢量预览") # 占位图，实际应用可生成缩略图
                                with open(os.path.join("assets/vectors", file_name), "rb") as f:
                                    st.download_button(
                                        label="⬇️ 下载 SVG",
                                        data=f,
                                        file_name=file_name,
                                        mime="image/svg+xml",
                                        use_container_width=True
                                    )

    # --- Tab 2: 外部资源导航 (新增功能) ---
    with tab2:
        st.markdown("### 找不到想要的？试试这些顶级开源库")
        st.markdown("以下网站提供海量免费、版权友好的生物医学插图。")
        
        # 资源 1: BioIcons
        with st.expander("🥇 BioIcons (强烈推荐)", expanded=True):
            c1, c2 = st.columns([1, 3])
            with c1:
                # 这里使用emoji代替图标，实际可以用logo图片
                st.markdown("# 🧬") 
            with c2:
                st.markdown("**BioIcons** 是目前最好的生物开源矢量库之一。")
                st.markdown("- **格式**: SVG (矢量)")
                st.markdown("- **版权**: 大部分为 CC0 (公有领域) 或 CC-BY (署名)。")
                st.link_button("访问 BioIcons 官网", "https://bioicons.com/")
        
        # 资源 2: SciDraw
        with st.expander("🥈 SciDraw (社区共建)"):
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("# 🐀")
            with c2:
                st.markdown("**SciDraw** 是由科学家为科学家建立的绘图库。")
                st.markdown("- **特点**: 包含复杂的解剖图和模式生物图。")
                st.markdown("- **注意**: 需仔细查看每个作者的具体版权要求。")
                st.link_button("访问 SciDraw 官网", "https://scidraw.io/")
        
        # 资源 3: Reactome
        with st.expander("🥉 Reactome Icon Library (专业通路)"):
            c1, c2 = st.columns([1, 3])
            with c1:
                st.markdown("# 🔄")
            with c2:
                st.markdown("**Reactome** 提供标准化的信号通路和分子图标。")
                st.markdown("- **适用**: 分子机制图、受体、配体、细胞器。")
                st.link_button("访问 Reactome 图标库", "https://reactome.org/icon-lib")

# --- 模块 3: 格式转换工具 ---
elif app_mode == "🛠️ 格式转换工具 (Tools)":
    st.title("🛠️ 出版级图片处理")
    st.markdown("将图片转换为符合 CNS 投稿标准的 **300 DPI** 格式。")
    
    uploaded_file = st.file_uploader("上传图片 (支持 JPG, PNG, TIFF)", type=['png', 'jpg', 'jpeg', 'tiff'])
    
    if uploaded_file:
        col1, col2 = st.columns(2)
        with col1:
            st.image(uploaded_file, caption="原始图片 preview", use_column_width=True)
        
        with col2:
            st.markdown("### 导出设置")
            target_format = st.radio("目标格式", ["TIFF (推荐)", "PNG"])
            
            if st.button("开始转换处理"):
                try:
                    # 调用 utils.py 中的函数
                    pil_img = convert_dpi(uploaded_file)
                    
                    # 准备下载流
                    buf = BytesIO()
                    save_format = "TIFF" if target_format.startswith("TIFF") else "PNG"
                    compression = "tiff_lzw" if save_format == "TIFF" else None
                    
                    pil_img.save(buf, format=save_format, dpi=(300, 300), compression=compression)
                    byte_im = buf.getvalue()
                    
                    st.success("✅ 转换完成！")
                    st.download_button(
                        label=f"⬇️ 下载 300 DPI {save_format}",
                        data=byte_im,
                        file_name=f"processed_300dpi.{save_format.lower()}",
                        mime=f"image/{save_format.lower()}"
                    )
                except Exception as e:
                    st.error(f"处理出错: {e}")

# 页脚
st.markdown("---")
st.caption("© 2025 BioMed Design Hub | Designed for Scientific Community")