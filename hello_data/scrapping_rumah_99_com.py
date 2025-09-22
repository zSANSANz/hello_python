import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import chromedriver_autoinstaller

# Install & pakai ChromeDriver otomatis
chromedriver_autoinstaller.install()

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # biar gak keliatan browsernya
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Buka halaman rumah dijual (contoh Jakarta)
url = "https://www.99.co/id/jual/rumah/jakarta"
driver.get(url)

# Tunggu data load
time.sleep(5)

# Ambil semua kartu listing
listings = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='listing-card-wrapper']")

data = []
for listing in listings:
    try:
        title = listing.find_element(By.CSS_SELECTOR, "h2").text
    except:
        title = ""

    try:
        price = listing.find_element(By.CSS_SELECTOR, "span[data-testid='listing-card-price']").text
    except:
        price = ""

    try:
        location = listing.find_element(By.CSS_SELECTOR, "span[data-testid='listing-card-address']").text
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
df.to_csv("99co_rumah.csv", index=False, encoding="utf-8-sig")
