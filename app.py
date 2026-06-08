import streamlit as st
import pandas as pd
import numpy as np
import random
import time

# ======================
# 頁面設定
# ======================
st.set_page_config(
    page_title="Sprint 5 AIoT微藻系統",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI微藻碳吸收最佳化系統（Sprint 5）")

# ======================
# 模式切換（整合 Sprint 3 + 4 + 5）
# ======================
mode = st.radio(
    "選擇模式",
    ["🎛️ 互動控制模式", "📊 Excel分析模式", "📡 IoT即時模式"]
)

# ======================
# AI模型（Sprint 5升級）
# ======================
def ai_model(light, temp, co2):
    return (
        0.45 * light +
        0.05 * co2 +
        (100 - abs(temp - 28) * 3)
    ) / 1.7

# ======================
# 🎛️ Sprint 3：互動模式
# ======================
if mode == "🎛️ 互動控制模式":

    st.subheader("互動環境控制")

    light = st.slider("光照強度", 0, 100, 80)
    temp = st.slider("溫度", 10, 40, 28)
    co2 = st.slider("CO₂濃度", 300, 1000, 600)

    efficiency = ai_model(light, temp, co2)
    co2_absorption = efficiency / 100 * 10

    st.metric("AI預測效率", f"{efficiency:.2f}%")
    st.metric("CO₂吸收量", f"{co2_absorption:.2f} kg")

# ======================
# 📊 Sprint 4：Excel分析模式
# ======================
elif mode == "📊 Excel分析模式":

    st.subheader("歷史資料分析")

    uploaded_file = st.file_uploader("上傳Excel", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("microalgae_simulated_data.xlsx")

    df.columns = df.columns.str.strip()

    st.dataframe(df)

    # 找 efficiency
    eff_col = [c for c in df.columns if "eff" in c.lower() or "效率" in c][0]

    best = df.loc[df[eff_col].idxmax()]

    st.subheader("最佳環境")

    st.write(best)

    st.line_chart(df[eff_col])

# ======================
# 📡 Sprint 5：IoT即時模式
# ======================
else:

    st.subheader("即時IoT模擬系統")

    placeholder = st.empty()

    history = []

    for i in range(30):

        light = random.randint(60, 100)
        temp = random.uniform(25, 32)
        co2 = random.randint(500, 800)

        efficiency = ai_model(light, temp, co2)

        history.append(efficiency)

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

        st.line_chart(history)

        time.sleep(0.8)

# ======================
# Sidebar（整合）
# ======================
st.sidebar.title("系統資訊")
st.sidebar.write("AI + IoT + Excel + Dashboard")