import time
import random
import json
from datetime import datetime
from urllib.parse import urlparse
import logging

import requests
import feedparser
from newspaper import Article
from bs4 import BeautifulSoup
import pandas as pd
from tqdm import tqdm

# --------- CONFIG ----------
USER_AGENT = "ResearchBot/1.0 (+https://example.com; contact: your-email@example.com)"
HEADERS = {"User-Agent": USER_AGENT}
REQUEST_TIMEOUT = 15
RATE_MIN, RATE_MAX = 1.0, 3.0  # seconds between requests

# Kata kunci untuk memfilter artikel relevan (bahasa Indonesia)
KEYWORDS = ["purbaya"]

# Daftar RSS feed dari beberapa media mainstream Indonesia (tambahkan sesuai kebutuhan)
RSS_FEEDS = {
    "detik": "https://rss.detik.com/index.php/indeks",
    "kompas": "https://rss.kompas.com/v1/?rss=terkini",
    "tempo": "https://rss.tempo.co/nasional",
    "cnnindonesia": "https://www.cnnindonesia.com/nasional/rss",
    "republika": "https://www.republika.co.id/rss/berita/nasional.xml",
    # tambahkan feed lain bila perlu
}

# Output files
OUT_JSON = "articles_korupsi.json"
OUT_CSV = "articles_korupsi.csv"

# Logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s: %(message)s")
# ----------------------------


def polite_sleep():
    time.sleep(random.uniform(RATE_MIN, RATE_MAX))


def contains_keyword(text, keywords=KEYWORDS):
    if not text:
        return False
    t = text.lower()
    return any(k.lower() in t for k in keywords)


def fetch_feed_items(feed_url, max_items=50):
    try:
        parsed = feedparser.parse(feed_url)
        return parsed.entries[:max_items]
    except Exception as e:
        logging.warning(f"Failed to parse feed {feed_url}: {e}")
        return []


def extract_with_newspaper(url):
    try:
        art = Article(url, language="id")
        art.download()
        art.parse()
        # art.nlp()  # optional: summary, keywords
        return {
            "title": art.title,
            "text": art.text,
            "authors": art.authors,
            "publish_date": art.publish_date.isoformat() if art.publish_date else None
        }
    except Exception as e:
        logging.debug(f"newspaper failed for {url}: {e}")
        return None


def extract_with_bs4(url):
    """Fallback generic extractor using BeautifulSoup (tries common tags)."""
    try:
        r = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "lxml")

        # Ambil title
        title_tag = soup.find("meta", property="og:title") or soup.find("title")
        title = title_tag.get("content") if title_tag and title_tag.has_attr("content") else (title_tag.text.strip() if title_tag else "")

        # Coba cari artikel berdasarkan tag umum
        selectors = [
            {"name": "article"},
            {"name": "div", "attrs": {"class": lambda v: v and "detail" in v.lower()}},
            {"name": "div", "attrs": {"class": lambda v: v and "artikel" in v.lower()}},
            {"name": "div", "attrs": {"class": lambda v: v and "content" in v.lower()}},
        ]

        content = ""
        for sel in selectors:
            node = soup.find(**sel)
            if node:
                # join all paragraphs
                ps = node.find_all("p")
                if ps:
                    content = "\n\n".join(p.get_text(strip=True) for p in ps)
                    break

        # last resort: all <p> in body
        if not content:
            body = soup.find("body")
            if body:
                ps = body.find_all("p")
                content = "\n\n".join(p.get_text(strip=True) for p in ps[:200])  # limit for safety

        # tanggal meta (jika ada)
        date_meta = None
        date_tag = soup.find("meta", property="article:published_time") or soup.find("meta", attrs={"name": "date"})
        if date_tag and date_tag.has_attr("content"):
            date_meta = date_tag["content"]

        return {
            "title": title.strip() if title else None,
            "text": content.strip() if content else None,
            "authors": None,
            "publish_date": date_meta
        }
    except Exception as e:
        logging.debug(f"BS4 failed for {url}: {e}")
        return None


def normalize_url(url, base=None):
    # simple normalization; can be expanded
    if url and url.startswith("//"):
        scheme = "https:"
        return scheme + url
    if url and url.startswith("/"):
        if base:
            p = urlparse(base)
            return f"{p.scheme}://{p.netloc}{url}"
    return url


def scrape():
    collected = []
    for source_name, feed in RSS_FEEDS.items():
        logging.info(f"Fetching feed: {source_name} -> {feed}")
        items = fetch_feed_items(feed, max_items=100)
        for entry in tqdm(items, desc=f"Feed {source_name}", leave=False):
            # entry fields vary: title, summary, link, published
            title = entry.get("title", "")
            summary = entry.get("summary", "") or entry.get("description", "")
            link = entry.get("link") or entry.get("guid")
            link = normalize_url(link, base=feed)
            published = entry.get("published") or entry.get("updated")

            # quick keyword filter on title/summary
            if not contains_keyword(title + " " + summary):
                # skip non-relevant article
                continue

            # polite
            polite_sleep()

            # Try to extract article content
            logging.info(f"Extracting: {link}")
            data = extract_with_newspaper(link)
            if (not data) or (not data.get("text")):
                data = extract_with_bs4(link)

            if not data:
                logging.warning(f"Failed to extract content from {link}")
                continue

            # basic sanity check: must have some text
            if not data.get("text") or len(data["text"]) < 50:
                logging.info(f"Too short or empty text for {link}, skipping.")
                continue

            record = {
                "source": source_name,
                "url": link,
                "title": data.get("title") or title,
                "summary": summary,
                "text": data.get("text"),
                "authors": data.get("authors"),
                "published": data.get("publish_date") or published,
                "scraped_at": datetime.utcnow().isoformat()
            }
            collected.append(record)

    logging.info(f"Scraped {len(collected)} articles matching keywords.")
    return collected


def save_outputs(records, json_path=OUT_JSON, csv_path=OUT_CSV):
    # Save JSON
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(records, f, ensure_ascii=False, indent=2)

    # Save CSV (flatten some fields)
    if records:
        df = pd.DataFrame(records)
        df.to_csv(csv_path, index=False, encoding="utf-8-sig")
    logging.info(f"Saved JSON -> {json_path}, CSV -> {csv_path}")


if __name__ == "__main__":
    records = scrape()
    save_outputs(records)
