import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Data
data = {
    "Open": [2590.4, 2626.5, 2636.8, 2656.3, 2662.3],
    "High": [2621.8, 2626.5, 2662.3, 2664.2, 2669.9],
    "Close": [2619.9, 2626.5, 2651.2, 2659.2, 2669.9]
}

df = pd.DataFrame(data)

# Variabel X dan Y
X = df[["Open", "High"]]
y = df["Close"]

# Model
model = LinearRegression()
model.fit(X, y)

# Koefisien
print("Intercept (a):", model.intercept_)
print("Koefisien b1 (Open):", model.coef_[0])
print("Koefisien b2 (High):", model.coef_[1])

# Prediksi contoh
prediksi = model.predict([[2640, 2660]])
print(f"Prediksi Close jika Open=2640 & High=2660: {prediksi[0]:.2f}")

# --- Visualisasi 3D ---
fig = plt.figure(figsize=(10, 7))
ax = fig.add_subplot(111, projection='3d')

# Scatter plot data asli
ax.scatter(df["Open"], df["High"], df["Close"], color='blue', label="Data Asli")

# Buat grid untuk bidang regresi
x_surf, y_surf = np.meshgrid(
    np.linspace(df["Open"].min(), df["Open"].max(), 10),
    np.linspace(df["High"].min(), df["High"].max(), 10)
)
z_surf = model.intercept_ + model.coef_[0]*x_surf + model.coef_[1]*y_surf

# Plot bidang regresi
ax.plot_surface(x_surf, y_surf, z_surf, alpha=0.3, color='red')

# Label
ax.set_xlabel("Open")
ax.set_ylabel("High")
ax.set_zlabel("Close")
ax.set_title("Regresi Linear Berganda: Prediksi Harga Emas")

plt.legend()
plt.show()
