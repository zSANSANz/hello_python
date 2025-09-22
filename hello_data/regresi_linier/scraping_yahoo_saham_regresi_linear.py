import pandas as pd
from sklearn.linear_model import LinearRegression

# Data (ambil dari tabel antum)
data = {
    "Open": [2581.2, 2570.7, 2566, 2590.4, 2626.5, 2636.8, 2656.3, 2662.3, 2670, 2660.9, 2631.4],
    "Close": [2564.3, 2570.7, 2588, 2619.9, 2626.5, 2651.2, 2659.2, 2669.9, 2644.3, 2636.1, 2667.3]
}

df = pd.DataFrame(data)

# Membuat model regresi linier
X = df[["Open"]]  # independen
y = df["Close"]   # dependen

model = LinearRegression()
model.fit(X, y)

# Koefisien dan intercept
a = model.intercept_
b = model.coef_[0]
print(f"Model Regresi Linier: Close = {a:.2f} + {b:.2f} * Open")

# Contoh prediksi
prediksi = model.predict([[2640]])  # prediksi jika Open = 2640
print(f"Prediksi Close untuk Open=2640: {prediksi[0]:.2f}")
