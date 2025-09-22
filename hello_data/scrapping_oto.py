import time
import csv
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

# install otomatis chromedriver sesuai versi Chrome
chromedriver_autoinstaller.install()

# set opsi Chrome headless
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")

driver = webdriver.Chrome(service=Service(), options=options)

url = "https://www.oto.com/mobil-bekas"
driver.get(url)
time.sleep(5)  # tunggu halaman load

cars = driver.find_elements(By.CSS_SELECTOR, ".listing-block")  # card mobil bekas

data = []
for car in cars:
    try:
        title = car.find_element(By.CSS_SELECTOR, ".title a").text.strip()
    except:
        title = ""
    try:
        harga = car.find_element(By.CSS_SELECTOR, ".price").text.strip()
    except:
        harga = ""
    try:
        lokasi = car.find_element(By.CSS_SELECTOR, ".city").text.strip()
    except:
        lokasi = ""
    try:
        link = car.find_element(By.CSS_SELECTOR, ".title a").get_attribute("href")
    except:
        link = ""

    if title:
        data.append([title, harga, lokasi, link])

driver.quit()

# Simpan ke CSV
with open("oto_mobil_bekas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["title", "harga", "lokasi", "link"])
    writer.writerows(data)

print(f"✅ Selesai, berhasil scrap {len(data)} mobil. Data tersimpan di oto_mobil_bekas.csv")
