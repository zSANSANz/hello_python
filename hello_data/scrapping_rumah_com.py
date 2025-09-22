import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import chromedriver_autoinstaller

# Install & pakai ChromeDriver otomatis
chromedriver_autoinstaller.install()

# Setup Selenium
options = webdriver.ChromeOptions()
options.add_argument("--headless")  # biar gak buka browser
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")

driver = webdriver.Chrome(options=options)

# Buka halaman rumah.com (contoh rumah dijual di Jakarta)
url = "https://www.rumah.com/rumah-dijual/di-jakarta"
driver.get(url)

# Tunggu halaman load
time.sleep(5)

# Ambil data rumah (judul, harga, lokasi, link)
listings = driver.find_elements(By.CSS_SELECTOR, "div[data-testid='listing-card']")

data = []
for listing in listings:
    try:
        title = listing.find_element(By.CSS_SELECTOR, "h3").text
    except:
        title = ""

    try:
        price = listing.find_element(By.CSS_SELECTOR, "span[data-testid='listing-price']").text
    except:
        price = ""

    try:
        location = listing.find_element(By.CSS_SELECTOR, "span[data-testid='listing-location']").text
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

# Tutup browser
driver.quit()

# Simpan ke CSV
df = pd.DataFrame(data)
print(df)
df.to_csv("rumah_com.csv", index=False, encoding="utf-8-sig")
