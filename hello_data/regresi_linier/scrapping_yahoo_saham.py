import yfinance as yf
import pandas as pd

# Contoh saham: Bank Central Asia (BCA) kode di Yahoo Finance = BBCA.JK
ticker = yf.Ticker("BBCA.JK")

# Ambil data historis 1 tahun terakhir
df = ticker.history(period="1y")

print(df.head())

# Simpan ke CSV
df.to_csv("scrapping_yahoo_bca.csv", index=True, encoding="utf-8-sig")
