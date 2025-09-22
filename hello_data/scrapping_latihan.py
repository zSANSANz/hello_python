import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By

# jalankan browser
driver = webdriver.Chrome()
driver.get("http://quotes.toscrape.com")

time.sleep(2)

data = []

quotes = driver.find_elements(By.CLASS_NAME, "quote")

for q in quotes:
    text = q.find_element(By.CLASS_NAME, "text").text
    author = q.find_element(By.CLASS_NAME, "author").text
    tags = [t.text for t in q.find_elements(By.CLASS_NAME, "tag")]
    data.append({
        "text": text,
        "author": author,
        "tags": ", ".join(tags)
    })

df = pd.DataFrame(data)
print(df)

df.to_csv("quotes.csv", index=False)

driver.quit()
