import pandas as pd
from sklearn.linear_model import LinearRegression

# Data fiktif dari yang antum kasih
data = {
    "Open": [2581.19995117187, 2570.69995117187, 2566, 2590.39990234375, 2626.5, 
             2636.80004882813, 2656.30004882812, 2662.30004882813, 2670, 2660.89990234375, 2631.39990234375],
    "Volume": [22, 25, 99, 17, 9, 35, 175, 17216, 4228, 973, 153],
    "Close": [2564.30004882812, 2570.69995117187, 2588, 2619.89990234375, 2626.5, 
              2651.19995117188, 2659.19995117188, 2669.89990234375, 2644.30004882812, 2636.10009765625, 2667.30004882812]
}

df = pd.DataFrame(data)

# Variabel independen dan dependen
X = df[["Open", "Volume"]]
y = df["Close"]

# Membuat model regresi linier berganda
model = LinearRegression()
model.fit(X, y)

# Intercept dan koefisien
print("Intercept (a):", model.intercept_)
print("Koefisien (b1, b2):", model.coef_)

# Prediksi contoh
prediksi = model.predict([[2650, 200]])  # Contoh: Open=2650, Volume=200
print("Prediksi Close:", prediksi[0])
