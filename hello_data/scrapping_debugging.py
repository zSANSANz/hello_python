# debug_chatnews.py
import requests
from urllib.parse import urljoin
import re
import time
import sys
import os

BASE = "https://chatnews.id"
TARGET = "https://chatnews.id/categories/kriptopedia"
ROBOTS = urljoin(BASE, "/robots.txt")

HEADERS_BASIC = {"User-Agent": "python-requests/2.x"}
HEADERS_BROWSER = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                  "Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "id-ID,id;q=0.9,en-US;q=0.8,en;q=0.7",
    "Referer": BASE
}

def check_robots():
    print("=== 1) Periksa robots.txt ===")
    try:
        r = requests.get(ROBOTS, headers=HEADERS_BROWSER, timeout=10)
        print("robots.txt status:", r.status_code)
        print("--- robots.txt (awal 400 chars) ---")
        print(r.text[:400].replace("\n", " "))
        # quick check if /categories path disallowed
        disallow = re.findall(r"Disallow:\s*(\S+)", r.text)
        if disallow:
            print("Disallow entries:", disallow[:10])
            if any(p.startswith("/categories") or p == "/categories" for p in disallow):
                print("WARNING: robots.txt explicitly disallows /categories path.")
            else:
                print("/categories not explicitly disallowed (by quick check).")
        else:
            print("No Disallow entries found (quick check).")
    except Exception as e:
        print("Gagal ambil robots.txt:", e)
    print()

def simple_request():
    print("=== 2) Request sederhana dengan requests (basic header) ===")
    try:
        r = requests.get(TARGET, headers=HEADERS_BASIC, timeout=10)
        print("Status code:", r.status_code)
        print("Content-type:", r.headers.get("content-type"))
        print("Content-length:", len(r.text))
        snippet = r.text[:800].replace("\n", " ")
        print("--- HTML snippet (first 800 chars) ---")
        print(snippet)
        return r
    except Exception as e:
        print("Request gagal:", e)
        return None
    finally:
        print()

def request_with_browser_headers():
    print("=== 3) Request dengan header browser (User-Agent) ===")
    try:
        r = requests.get(TARGET, headers=HEADERS_BROWSER, timeout=10)
        print("Status code:", r.status_code)
        print("Content-type:", r.headers.get("content-type"))
        print("Content-length:", len(r.text))
        snippet = r.text[:800].replace("\n", " ")
        print("--- HTML snippet (first 800 chars) ---")
        print(snippet)
        return r
    except Exception as e:
        print("Request gagal:", e)
        return None
    finally:
        print()

def scan_for_protection_markers(html):
    print("=== 4) Scan HTML untuk tanda proteksi / blokir ===")
    markers = [
        "Access denied", "access denied", "Domain not allowed", "403 Forbidden",
        "captcha", "please enable javascript", "jschl_vc", "__cf_chl_jschl_tk__",
        "Cloudflare", "DDoS protection", "Checking your browser before accessing",
        "bot verification", "recaptcha", "hCaptcha"
    ]
    found = []
    low = html.lower()
    for m in markers:
        if m.lower() in low:
            found.append(m)
    if found:
        print("Tanda proteksi ditemukan:", found)
    else:
        print("Tidak menemukan tanda proteksi umum di HTML snippet.")
    # also look for meta refresh to a challenge or javascript heavy content
    if re.search(r"window\.location|location\.href|document\.write", html, re.I):
        print("Ada indikasi redirect via JS (window.location / document.write).")
    # look for Cloudflare challenge snippet
    if "__cf_chl_" in html or "cloudflare" in low:
        print("Ada kata-kata terkait Cloudflare.")
    print()

def search_for_content_markers(html):
    print("=== 5) Cari elemen artikel / link di HTML ===")
    checks = {
        "has_article_tag": bool(re.search(r"<article\b", html, re.I)),
        "has_time_tag": bool(re.search(r"<time\b", html, re.I)),
        "posts_pattern_/posts/": bool(re.search(r"href=[\"'](/posts/[^\"']+)[\"']", html)),
        "has_post_list": bool(re.search(r"class=[\"'][^\"'>]*post[^\"]*[\"']", html, re.I)),
        "has_ld_json": bool(re.search(r"<script[^>]*type=[\"']application/ld\+json[\"']>", html, re.I)),
        "has_api_strings": bool(re.search(r"/api/|graphql|data-qa-id|data-testid", html, re.I))
    }
    for k, v in checks.items():
        print(f"{k}: {v}")
    # show a few matches of /posts/ if present
    posts = re.findall(r"href=[\"'](/posts/[^\"']+)[\"']", html)
    if posts:
        print("Sample post hrefs (up to 10):")
        for p in posts[:10]:
            print("  -", urljoin(BASE, p))
    print()

def try_find_api_endpoints(html):
    print("=== 6) Cari indikasi API endpoint di HTML (json endpoints) ===")
    apis = re.findall(r"['\"](https?://[^'\" ]+/api/[^'\" ]+)['\"]", html)
    apis += re.findall(r"(/api/[^'\" ]+)", html)
    apis = list(dict.fromkeys(apis))
    if apis:
        print("Ditemukan potensi API endpoints (sample up to 10):")
        for a in apis[:10]:
            print("  -", a)
    else:
        print("Tidak menemukan pola '/api/' atau graphql endpoint di HTML.")
    print()

def run_selenium_check():
    try:
        from selenium import webdriver
        from selenium.webdriver.common.by import By
        import chromedriver_autoinstaller
    except Exception as e:
        print("=== 7) Selenium check SKIPPED ===")
        print("Selenium / chromedriver tidak terpasang di environment ini.")
        print("Jika mau, install chromedriver-autoinstaller dan selenium:")
        print("  pip install selenium chromedriver-autoinstaller")
        print()
        return

    print("=== 7) Selenium check (headless) ===")
    chromedriver_autoinstaller.install()
    from selenium.webdriver.chrome.options import Options
    options = Options()
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=options)
    try:
        driver.set_page_load_timeout(30)
        driver.get(TARGET)
        time.sleep(5)  # tunggu render
        page_source = driver.page_source
        print("Selenium fetched page length:", len(page_source))
        out_png = "chatnews_debug_screenshot.png"
        driver.save_screenshot(out_png)
        print("Screenshot saved to", out_png)
        if "<article" in page_source.lower():
            print("Selenium: artikel TAG ditemukan di page_source.")
        else:
            print("Selenium: TIDAK menemukan <article> tag di page_source.")
        els = driver.find_elements(By.CSS_SELECTOR, "a")
        hrefs = []
        for e in els[:200]:
            try:
                h = e.get_attribute("href")
                if h and "/posts/" in h:
                    hrefs.append(h)
            except:
                pass
        print("Selenium: found /posts/ links sample:", hrefs[:10])
    except Exception as e:
        print("Selenium error:", e)
    finally:
        driver.quit()
    print()
