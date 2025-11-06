import pandas as pd
import matplotlib.pyplot as plt

# Baca data dari file CSV yang sudah di-scraping
df = pd.read_csv("scrapping_yahoo_bca.csv")

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
x_pred = 7250  
y_pred = a + b * x_pred
print(f"\nPrediksi Close jika Open={x_pred}: {y_pred}")

# -----------------------------
# 6. Gambar grafik regresi
# -----------------------------
plt.figure(figsize=(8,6))

# Scatter data asli
plt.scatter(df["Open"], df["Close"], color="blue", label="Data Asli")

# Garis regresi (manual pakai a + bX)
x_line = [df["Open"].min(), df["Open"].max()]
y_line = [a + b*x for x in x_line]
plt.plot(x_line, y_line, color="red", label="Garis Regresi")

# Titik prediksi
plt.scatter(x_pred, y_pred, color="green", s=100, marker="x", label=f"Prediksi (Open={x_pred})")

# Label & Judul
plt.xlabel("Open Price")
plt.ylabel("Close Price")
plt.title("Regresi Linier Manual (Open vs Close)")
plt.legend()
plt.grid(True)
plt.show()
