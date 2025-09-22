import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

# Install & pakai ChromeDriver otomatis
chromedriver_autoinstaller.install()

options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Contoh pencarian rumah dijual di Jakarta
url = "https://www.olx.co.id/properti/rumah/jual/jakarta-dki-jakarta"
driver.get(url)

time.sleep(5)

# Ambil semua listing
listings = driver.find_elements(By.CSS_SELECTOR, "div[data-aut-id='itemBox']")

data = []
for listing in listings:
    try:
        title = listing.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemTitle']").text
    except:
        title = ""

    try:
        price = listing.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemPrice']").text
    except:
        price = ""

    try:
        location = listing.find_element(By.CSS_SELECTOR, "span[data-aut-id='itemLocation']").text
    except:
        location = ""

    try:
        link = listing.find_element(By.TAG_NAME, "a").get_attribute("href")
    except:
        link = ""

    data.append({
        "title": title,
        "price": price,
        "location": location,
        "link": link
    })

driver.quit()

# Simpan ke CSV
df = pd.DataFrame(data)
print(df)
df.to_csv("olx_rumah.csv", index=False, encoding="utf-8-sig")
