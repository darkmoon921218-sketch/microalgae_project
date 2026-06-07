import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

# 讀取 Excel 資料
df = pd.read_excel("microalgae_simulated_data.xlsx")

# 顯示前五筆資料
print("資料預覽：")
print(df.head())
print(f"\n資料形狀: {df.shape}")

# 檢查缺失值
print("\n檢查缺失值:")
print(df.isnull().sum())

# 特徵（輸入）
X = df[["Light", "Temp", "CO2"]]
y = df["Efficiency"]

# 建立和訓練模型
model = LinearRegression()
model.fit(X, y)

# 顯示各因素影響程度
print("\n各因素影響程度：")
print(f"Light 係數: {model.coef_[0]:.4f}")
print(f"Temp 係數: {model.coef_[1]:.4f}")
print(f"CO2 係數: {model.coef_[2]:.4f}")
print(f"截距: {model.intercept_:.4f}")

# 模型評估
y_pred = model.predict(X)
r2 = r2_score(y, y_pred)
rmse = mean_squared_error(y, y_pred) ** 0.5

print(f"\n模型性能：")
print(f"R² 分數: {r2:.4f}")
print(f"均方根誤差: {rmse:.4f}")

# 預測最佳條件
sample = [[80, 28, 600]]
prediction = model.predict(sample)

print("\n預測結果：")
print(f"在 Light=80、Temp=28、CO2=600 時")
print(f"預測吸收效率為: {prediction[0]:.2f}%")

# 簡化的圖表生成函數
def plot_and_save(x_col, y_col, filename):
    """繪製散點圖並保存"""
    plt.figure(figsize=(8, 5))
    plt.scatter(df[x_col], df[y_col], alpha=0.6)
    plt.xlabel(x_col, fontsize=12)
    plt.ylabel(y_col, fontsize=12)
    plt.title(f"{x_col} vs {y_col}", fontsize=14)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(filename, dpi=100)
    plt.close()

# 生成三個圖表
plot_and_save("Light", "Efficiency", "light_efficiency.png")
plot_and_save("Temp", "Efficiency", "temp_efficiency.png")
plot_and_save("CO2", "Efficiency", "co2_efficiency.png")

print("\n✅ 圖表已儲存完成！")
print("輸出檔案：")
print("- light_efficiency.png")
print("- temp_efficiency.png")
print("- co2_efficiency.png")