import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import numpy as np

# Data (ambil dari tabel antum)
data = {
    "Open": [2581.2, 2570.7, 2566, 2590.4, 2626.5, 2636.8, 2656.3, 2662.3, 2670, 2660.9, 2631.4],
    "Close": [2564.3, 2570.7, 2588, 2619.9, 2626.5, 2651.2, 2659.2, 2669.9, 2644.3, 2636.1, 2667.3]
}

df = pd.DataFrame(data)

# Membuat model regresi linier
X = df[["Open"]]
y = df["Close"]

model = LinearRegression()
model.fit(X, y)

# Koefisien dan intercept
a = model.intercept_
b = model.coef_[0]
print(f"Model Regresi Linier: Close = {a:.2f} + {b:.2f} * Open")

# Buat garis regresi
X_range = np.linspace(df["Open"].min(), df["Open"].max(), 100).reshape(-1, 1)
y_pred = model.predict(X_range)

# Plot
plt.figure(figsize=(8,5))
plt.scatter(df["Open"], df["Close"], color="blue", label="Data Aktual")
plt.plot(X_range, y_pred, color="red", linewidth=2, label="Regresi Linier")
plt.xlabel("Open")
plt.ylabel("Close")
plt.title("Hubungan Open vs Close (Regresi Linier)")
plt.legend()
plt.grid(True)
plt.show()
