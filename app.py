import streamlit as st
import pandas as pd
import numpy as np
import time
import random

# ======================
# 頁面設定
# ======================
st.set_page_config(
    page_title="Sprint 5 - AIoT微藻碳吸收系統",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 Sprint 5 - AIoT微藻碳吸收系統")

st.markdown("智慧碳中和園區｜AI + IoT 即時碳吸收監測系統")

# ======================
# 模式切換
# ======================
mode = st.radio(
    "選擇模式",
    ["📊 歷史資料模式 (Excel)", "📡 IoT即時模擬模式"]
)

# ======================
# AI簡易模型（可替換成ML）
# ======================
def ai_model(light, temp, co2):
    return (
        0.45 * light +
        0.05 * co2 +
        (100 - abs(temp - 28) * 3)
    ) / 1.7

# ======================
# 📊 模式1：歷史資料
# ======================
if mode == "📊 歷史資料模式 (Excel)":

    st.subheader("📂 上傳歷史資料")

    uploaded_file = st.file_uploader("上傳 Excel", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
    else:
        df = pd.read_excel("microalgae_simulated_data.xlsx")

    df.columns = df.columns.str.strip()

    st.subheader("📊 歷史資料")
    st.dataframe(df)

    # 找 Efficiency
    eff_col = [c for c in df.columns if "eff" in c.lower() or "效率" in c][0]

    st.subheader("📈 效率趨勢")
    if "日期" in df.columns:
        df["日期"] = pd.to_datetime(df["日期"])
        st.line_chart(df.set_index("日期")[eff_col])

    best = df.loc[df[eff_col].idxmax()]

    st.subheader("🏆 最佳條件")

    for col in df.columns:
        if col != eff_col:
            st.write(f"{col}：{best[col]}")

    st.write(f"Efficiency：{best[eff_col]:.2f}%")

# ======================
# 📡 模式2：IoT即時模擬
# ======================
else:

    st.subheader("📡 即時 IoT 感測模擬")

    placeholder = st.empty()
    chart_placeholder = st.line_chart([])

    history = []

    for i in range(50):

        # 模擬IoT數據
        light = random.randint(60, 100)
        temp = random.uniform(25, 32)
        co2 = random.randint(500, 800)

        efficiency = ai_model(light, temp, co2)

        history.append([light, temp, co2, efficiency])

        df_live = pd.DataFrame(history, columns=["Light", "Temp", "CO2", "Efficiency"])

        # 即時畫面
        with placeholder.container():

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("光照", f"{light}")
            col2.metric("溫度", f"{temp:.1f}°C")
            col3.metric("CO₂", f"{co2}")
            col4.metric("效率", f"{efficiency:.2f}%")

            if efficiency > 90:
                st.success("最佳吸收狀態")
            elif efficiency > 75:
                st.warning("中等效率")
            else:
                st.error("效率偏低")

        chart_placeholder.line_chart(df_live.set_index(pd.Index(range(len(df_live))))["Efficiency"])

        time.sleep(1)

# ======================
# Sidebar
# ======================
st.sidebar.title("系統資訊")
st.sidebar.write("Sprint 5 - AIoT版本")
st.sidebar.write("AI + IoT + Dashboard")