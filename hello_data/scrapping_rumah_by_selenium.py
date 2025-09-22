import time
import pandas as pd
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Auto install driver sesuai versi Chrome
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")  # bisa dihapus kalau mau lihat browsernya
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# URL contoh
url = "https://www.rumah123.com/jual/dki-jakarta/rumah/"
driver.get(url)
time.sleep(5)

# scroll biar semua listing muncul
body = driver.find_element(By.TAG_NAME, "body")
for _ in range(5):  # scroll 5x
    body.send_keys(Keys.END)
    time.sleep(2)

cards = driver.find_elements(By.CSS_SELECTOR, "div[data-qa-id='listing-card-wrapper']")

records = []
for card in cards:
    try:
        title = card.find_element(By.CSS_SELECTOR, "a[data-qa-id='title']").text
        price = card.find_element(By.CSS_SELECTOR, "div[data-qa-id='listing-price']").text
        location = card.find_element(By.CSS_SELECTOR, "div[data-qa-id='listing-location']").text

        specs = card.find_elements(By.CSS_SELECTOR, "div[data-qa-id='listing-spec']")
        luas_bangunan, luas_tanah = None, None
        for spec in specs:
            txt = spec.text.lower()
            if "m²" in txt:
                if luas_bangunan is None:
                    luas_bangunan = txt
                else:
                    luas_tanah = txt

        records.append({
            "title": title,
            "price": price,
            "location": location,
            "luas_bangunan": luas_bangunan,
            "luas_tanah": luas_tanah
        })
    except Exception as e:
        print("Skip:", e)

driver.quit()

df = pd.DataFrame(records)
print(df.head())
df.to_csv("rumah123.csv", index=False)
