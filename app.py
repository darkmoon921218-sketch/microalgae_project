import streamlit as st
import pandas as pd

# ======================
# 頁面設定
# ======================
st.set_page_config(
    page_title="AI微藻碳吸收最佳化系統",
    page_icon="🌱",
    layout="wide"
)

st.title("🌱 AI微藻碳吸收最佳化系統")

st.markdown("""
本系統利用 AI 分析微藻碳吸收效率，
協助智慧碳中和園區進行最佳化管理。
""")

# ======================
# 使用者輸入
# ======================
col1, col2, col3 = st.columns(3)

with col1:
    light = st.slider("光照強度", 0, 100, 80)

with col2:
    temp = st.slider("溫度 (°C)", 10, 40, 28)

with col3:
    co2 = st.slider("CO₂濃度 (ppm)", 300, 1000, 600)

# ======================
# AI模型（簡化版）
# ======================
efficiency = (
    0.4 * light
    + 0.05 * co2
    + (100 - abs(temp - 28) * 3)
) / 1.6

st.metric("預測吸收效率", f"{efficiency:.1f}%")

# ======================
# CO₂吸收量
# ======================
co2_absorption = efficiency / 100 * 10
st.metric("每日CO₂吸收量", f"{co2_absorption:.2f} kg")

# ======================
# 環境狀態
# ======================
st.subheader("🌿 環境狀態")

if efficiency >= 90:
    st.success("微藻目前處於最佳吸收狀態")
elif efficiency >= 75:
    st.warning("微藻吸收效率普通，可進一步優化")
else:
    st.error("吸收效率偏低，建議調整環境")

# ======================
# AI建議
# ======================
st.subheader("🤖 AI最佳化建議")

if temp < 28:
    st.write("建議提高溫度至 28°C")
elif temp > 28:
    st.write("建議降低溫度至 28°C")

if light < 80:
    st.write("建議提高光照強度")

if co2 < 600:
    st.write("建議提高 CO₂ 濃度")

if temp > 30:
    st.warning("溫度過高")

if co2 < 500:
    st.warning("建議增加 CO₂")

# ======================
# 上傳 Excel
# ======================
st.subheader("📂 上傳資料")

uploaded_file = st.file_uploader("請上傳 Excel 檔案", type=["xlsx"])

if uploaded_file is not None:
    df = pd.read_excel(uploaded_file)
    st.success("檔案上傳成功")
else:
    df = pd.read_excel("microalgae_simulated_data.xlsx")

# ======================
# 清理欄位（超重要）
# ======================
df.columns = df.columns.str.strip()

# Excel 的 Efficiency → 統一成 Efficiency
if "Efficiency" in df.columns:
    eff_col = "Efficiency"
else:
    st.error("❌ 找不到 Efficiency 欄位")
    st.write(df.columns)
    st.stop()

# ======================
# 顯示資料
# ======================
st.subheader("📊 歷史資料")
st.dataframe(df)

# ======================
# 最佳環境條件
# ======================
st.subheader("🏆 最佳環境條件")

best = df.loc[df[eff_col].idxmax()]

# 自動抓欄位（避免不同Excel格式炸掉）
def find_col(keywords):
    for c in df.columns:
        if any(k in c.lower() for k in keywords):
            return c
    return None

light_col = find_col(["light", "光"])
temp_col = find_col(["temp", "溫"])
co2_col = find_col(["co2", "co₂"])

if light_col:
    st.write(f"最佳光照強度：{best[light_col]}")

if temp_col:
    st.write(f"最佳溫度：{best[temp_col]} °C")

if co2_col:
    st.write(f"最佳CO₂濃度：{best[co2_col]}")

st.write(f"最高吸收效率：{best[eff_col]:.2f}%")

# ======================
# 折線圖
# ======================
st.subheader("📈 吸收效率趨勢圖")

if "日期" in df.columns:
    df["日期"] = pd.to_datetime(df["日期"])
    chart_df = df.set_index("日期")
    st.line_chart(chart_df[eff_col])

# ======================
# 長條圖
# ======================
st.subheader("📊 光照 vs 吸收效率")

if light_col:
    st.bar_chart(df[[light_col, eff_col]])

# ======================
# 圖片
# ======================
st.subheader("📷 歷史圖表")

st.image("light_efficiency.png")
st.image("temp_efficiency.png")
st.image("co2_efficiency.png")

# ======================
# Sidebar
# ======================
st.sidebar.title("系統資訊")
st.sidebar.write("AI微藻碳吸收最佳化系統")
st.sidebar.write(f"目前效率：{efficiency:.1f}%")
st.sidebar.write(f"每日吸收量：{co2_absorption:.2f} kg")