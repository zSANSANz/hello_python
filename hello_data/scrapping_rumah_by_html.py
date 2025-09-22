import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://www.rumah123.com/jual/dki-jakarta/rumah/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

res = requests.get(url, headers=headers)
soup = BeautifulSoup(res.text, "html.parser")

records = []
for card in soup.select("div[data-qa-id='listing-card']"):
    title = card.get("title") or ""
    price = card.select_one("div[data-qa-id='listing-price']")
    location = card.select_one("div[data-qa-id='listing-location']")
    specs = card.select("li[data-qa-id='listing-spec']")

    luas_bangunan, luas_tanah = None, None
    for spec in specs:
        txt = spec.get_text(strip=True)
        if "m²" in txt and "Bangunan" in txt:
            luas_bangunan = txt.replace("Bangunan", "").strip()
        if "m²" in txt and "Tanah" in txt:
            luas_tanah = txt.replace("Tanah", "").strip()

    records.append({
        "title": title,
        "price": price.get_text(strip=True) if price else None,
        "location": location.get_text(strip=True) if location else None,
        "luas_bangunan": luas_bangunan,
        "luas_tanah": luas_tanah
    })

df = pd.DataFrame(records)
print(df.head())
