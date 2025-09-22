import yfinance as yf
import pandas as pd

# Contoh saham: Future Gold kode di Yahoo Finance = GC=F
ticker = yf.Ticker("GC=F")

# Ambil data historis 1 tahun terakhir
df = ticker.history(period="1y")

print(df.head())

# Simpan ke CSV
df.to_csv("scrapping_yahoo_emas.csv", index=True, encoding="utf-8-sig")
