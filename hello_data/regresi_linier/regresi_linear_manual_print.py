import pandas as pd

# Data
data = {
    "Open": [2581.2, 2570.7, 2566, 2590.4, 2626.5, 2636.8, 2656.3, 2662.3, 2670, 2660.9, 2631.4],
    "Close": [2564.3, 2570.7, 2588, 2619.9, 2626.5, 2651.2, 2659.2, 2669.9, 2644.3, 2636.1, 2667.3]
}
df = pd.DataFrame(data)

# 1. Hitung rata-rata
x_mean = df["Open"].mean()
y_mean = df["Close"].mean()
print("Rata-rata Open (x̄):", x_mean)
print("Rata-rata Close (ȳ):", y_mean)

# 2. Hitung deviasi
df["x_dev"] = df["Open"] - x_mean
df["y_dev"] = df["Close"] - y_mean
df["x_dev*y_dev"] = df["x_dev"] * df["y_dev"]
df["x_dev^2"] = df["x_dev"] ** 2

print("\nTabel Perhitungan:")
print(df)

# 3. Hitung jumlah
sum_xy = df["x_dev*y_dev"].sum()
sum_x2 = df["x_dev^2"].sum()
print("\nΣ(x_dev * y_dev):", sum_xy)
print("Σ(x_dev^2):", sum_x2)

# 4. Hitung slope (b) dan intercept (a)
b = sum_xy / sum_x2
a = y_mean - b * x_mean
print("\nSlope (b):", b)
print("Intercept (a):", a)

# 5. Prediksi contoh
x_pred = 2640
y_pred = a + b * x_pred
print(f"\nPrediksi Close jika Open={x_pred}: {y_pred}")
