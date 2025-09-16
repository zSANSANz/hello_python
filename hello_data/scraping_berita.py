import feedparser

# Daftar RSS feed berita nasional
rss_feeds = {
    "Republika": "https://www.republika.co.id/rss/",
    "Kompas": "https://www.kompas.com/rss",
    "Detik": "https://rss.detik.com/index.php/detikcom",
    "Tempo": "https://rss.tempo.co/"
}

def get_news(feed_url, source_name, limit=5):
    feed = feedparser.parse(feed_url)
    print(f"\n📌 {source_name} - {len(feed.entries)} berita ditemukan")
    for entry in feed.entries[:limit]:  # ambil berita sesuai limit
        print(f"- {entry.title}")
        print(f"  Link: {entry.link}")
        if hasattr(entry, "published"):
            print(f"  Tanggal: {entry.published}")
        print()

# Jalankan scraping dari semua sumber
for source, url in rss_feeds.items():
    get_news(url, source)
