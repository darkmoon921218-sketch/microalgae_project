import streamlit as st
import pandas as pd
import numpy as np
import random

# ======================
# 頁面設定
# ======================
st.set_page_config(
    page_title="AI微藻碳吸收最佳化系統",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI微藻碳吸收最佳化系統（Sprint 5）")

st.markdown("""
本系統整合 AI + IoT + Excel 分析，
用於微藻碳吸收最佳化模擬。
""")

# ======================
# Sidebar（一定要放最外層）
# ======================
st.sidebar.title("系統資訊")
st.sidebar.write("AI微藻碳吸收系統")
st.sidebar.write("Sprint 5 完整版本")

# ======================
# AI 模型
# ======================
def ai_model(light, temp, co2):
    return (
        0.45 * light +
        0.05 * co2 +
        (100 - abs(temp - 28) * 3)
    ) / 1.7


# ======================
# 模式切換（Sprint整合）
# ======================
mode = st.radio(
    "選擇模式",
    ["🎛️ 互動模式", "📊 Excel分析", "📡 IoT即時模式"]
)

# =========================================================
# 🎛️ Sprint 3：互動模式
# =========================================================
if mode == "🎛️ 互動模式":

    st.subheader("環境控制")

    light = st.slider("光照強度", 0, 100, 80)
    temp = st.slider("溫度", 10, 40, 28)
    co2 = st.slider("CO₂濃度", 300, 1000, 600)

    efficiency = ai_model(light, temp, co2)
    co2_absorption = efficiency / 100 * 10

    st.metric("AI預測效率", f"{efficiency:.2f}%")
    st.metric("CO₂吸收量", f"{co2_absorption:.2f} kg")

    if efficiency > 90:
        st.success("最佳狀態")
    elif efficiency > 75:
        st.warning("中等狀態")
    else:
        st.error("低效率")

# =========================================================
# 📊 Sprint 4：Excel分析
# =========================================================
elif mode == "📊 Excel分析":

    st.subheader("歷史資料分析")

    uploaded_file = st.file_uploader("上傳 Excel", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("microalgae_simulated_data.xlsx")

    df.columns = df.columns.str.strip()

    st.dataframe(df)

    # 自動找 efficiency 欄位
    eff_col = None
    for c in df.columns:
        if "eff" in c.lower() or "效率" in c:
            eff_col = c
            break

    if eff_col is None:
        st.error("找不到 Efficiency 欄位")
        st.stop()

    # 最佳值
    best = df.loc[df[eff_col].idxmax()]

    st.subheader("最佳環境條件")
    st.write(best)

    # 圖表
    st.line_chart(df[eff_col])

    if "光照強度" in df.columns:
        st.bar_chart(df[["光照強度", eff_col]])

# =========================================================
# 📡 Sprint 5：IoT 即時模式（已修正）
# =========================================================
else:

    st.subheader("即時 IoT 模擬系統")

    if "history" not in st.session_state:
        st.session_state.history = []

    placeholder = st.empty()
    chart = st.empty()

    # ===== 模擬 IoT資料 =====
    light = random.randint(60, 100)
    temp = random.uniform(25, 32)
    co2 = random.randint(500, 800)

    efficiency = ai_model(light, temp, co2)

    # 記錄歷史
    st.session_state.history.append(efficiency)

    if len(st.session_state.history) > 30:
        st.session_state.history.pop(0)

    # ===== UI更新（不洗版） =====
    with placeholder.container():

        col1, col2, col3, col4 = st.columns(4)

        col1.metric("光照", light)
        col2.metric("溫度", f"{temp:.1f}")
        col3.metric("CO₂", co2)
        col4.metric("效率", f"{efficiency:.2f}%")

        if efficiency > 90:
            st.success("最佳吸收狀態")
        elif efficiency > 75:
            st.warning("中等效率")
        else:
            st.error("效率偏低")

    # ===== 圖表（只更新同一張） =====
    chart.line_chart(st.session_state.history)

    # 手動更新按鈕（避免自動洗版）
    st.button("更新模擬數據")