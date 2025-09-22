import time
import requests
from bs4 import BeautifulSoup
import pandas as pd
from urllib.parse import urljoin

BASE = "https://chatnews.id"
START_URL = "https://chatnews.id/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; ResearchBot/1.0; +mailto:youremail@example.com)"
}

def get_article_links(page_url):
    r = requests.get(page_url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    links = []
    for a in soup.select("a"):
        href = a.get("href", "")
        if href and "/posts/" in href:
            links.append(urljoin(BASE, href))

    # cari link pagination "Next"
    next_page = None
    next_btn = soup.find("a", string="Next")  # sesuaikan kalau beda
    if next_btn:
        next_page = urljoin(BASE, next_btn.get("href"))

    return list(dict.fromkeys(links)), next_page

def fetch_article(url):
    r = requests.get(url, headers=HEADERS, timeout=10)
    soup = BeautifulSoup(r.text, "html.parser")

    title = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    date = soup.find("time").get_text(strip=True) if soup.find("time") else None
    paragraphs = [p.get_text(strip=True) for p in soup.select("article p")]
    text = "\n".join(paragraphs)

    return {"url": url, "title": title, "date": date, "text": text}

def main():
    all_links = []
    page_url = START_URL

    # loop pagination
    while page_url:
        print("Scraping halaman:", page_url)
        links, next_page = get_article_links(page_url)
        all_links.extend(links)
        page_url = next_page
        time.sleep(2)

    print("Total links ditemukan:", len(all_links))

    records = []
    for i, link in enumerate(all_links, 1):
        print(f"[{i}/{len(all_links)}] Fetching:", link)
        try:
            rec = fetch_article(link)
            records.append(rec)
        except Exception as e:
            print("skip", link, e)
        time.sleep(2)

    df = pd.DataFrame(records)
    df.to_csv("chatnews_kriptopedia.csv", index=False, encoding="utf-8-sig")
    print("Saved", len(df), "articles.")

if __name__ == "__main__":
    main()
