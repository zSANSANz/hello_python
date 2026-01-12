from nitter_scraper import NitterScraper
import pandas as pd

scraper = NitterScraper()

query = "purbaya"
tweets = scraper.search(query, mode="latest", number=200)

data = []
for t in tweets:
    data.append([t.date, t.username, t.text])

df = pd.DataFrame(data, columns=["date", "username", "content"])
df.to_csv("tweets_purbaya.csv", index=False)

print(df.head())
