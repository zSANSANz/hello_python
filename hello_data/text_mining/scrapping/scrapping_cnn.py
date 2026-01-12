import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://www.cnnindonesia.com/nasional"
response = requests.get(base_url)
soup = BeautifulSoup(response.text, "html.parser")

articles = soup.find_all("article")

data = []
for art in articles:
    try:
        title = art.find("h2", class_="title").get_text(strip=True)
    except:
        title = ""
    try:
        link = art.find("a")["href"]
    except:
        link = ""
    try:
        date = art.find("span", class_="date").get_text(strip=True)
    except:
        date = ""

    data.append({
        "title": title,
        "link": link,
        "date": date
    })

df = pd.DataFrame(data)
print(df)
df.to_csv("cnnindonesia_news.csv", index=False, encoding="utf-8-sig")
