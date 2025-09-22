import requests
from bs4 import BeautifulSoup
import pandas as pd

url = "https://chatnews.id/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

resp = requests.get(url, headers=headers)
print("STATUS:", resp.status_code)

soup = BeautifulSoup(resp.text, "html.parser")

# coba lihat semua artikel
articles = soup.find_all("article")
print("Jumlah artikel ditemukan:", len(articles))

data = []
for art in articles:
    # title
    title_tag = art.find("h2")
    title = title_tag.text.strip() if title_tag else None

    # link
    link_tag = art.find("a")
    link = link_tag["href"] if link_tag and link_tag.has_attr("href") else None

    # category
    category_tag = art.find("a", class_="category")
    category = category_tag.text.strip() if category_tag else None

    # date
    date_tag = art.find("time")
    date = date_tag.text.strip() if date_tag else None

    # debugging
    print("DEBUG =>", title, "|", link, "|", category, "|", date)

    data.append({
        "title": title,
        "link": link,
        "category": category,
        "date": date
    })

# simpan ke CSV
df = pd.DataFrame(data)
df.to_csv("chatnews.csv", index=False, encoding="utf-8-sig")

print("CSV berhasil dibuat: chatnews.csv")
print(df.head())
