import requests
import pandas as pd

url = "https://www.rumah123.com/api/property/nearest-pdp-list/"

headers = {
    "accept": "*/*",
    "authorization": "Basic OTlncm91cDp0ZWFtMXN0ISEh",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"
}

# body request → 
payload = {"lat": -6.9175, "long": 107.6191}

response = requests.post(url, headers=headers, json=payload)

print("STATUS:", response.status_code)
print("RAW TEXT:", response.text[:500])  # print 500 char pertama

try:
    data = response.json()
    print("JSON KEYS:", data.keys())
except Exception as e:
    print("Error parsing JSON:", e)
    data = {}

# Ambil field penting
records = []
for item in data:
    records.append({
        "title": item.get("title"),
        "price": item.get("price"),
        "location": item.get("locationWithProvince"),
        "url": "https://www.rumah123.com" + item.get("url", "")
    })

df = pd.DataFrame(records)
print(df.head())
