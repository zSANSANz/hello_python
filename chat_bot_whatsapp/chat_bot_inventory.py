from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import time

# Inisialisasi browser (pastikan ChromeDriver sesuai versi Chrome sudah ada di PATH)
driver = webdriver.Chrome()
driver.get("https://web.whatsapp.com")

print("Scan QR Code di browser... (waktu tunggu 20 detik)")
time.sleep(20)

# Tutup popup "Your chats and calls are private" kalau muncul
try:
    ok_button = driver.find_element(By.XPATH, '//button[@aria-label="OK"]')
    ok_button.click()
    print("Popup enkripsi ditutup otomatis")
except NoSuchElementException:
    print("Tidak ada popup enkripsi")

# Menyimpan sesi chat user
sessions = {}


# Pertanyaan form
def tanya(step):
    pertanyaan = {
        1: "Selamat datang di layanan kek it inventory, apakah anda sudah mempunyai akses ke website itinventory?",
        2: "Masukkan Nama Perusahaan anda",
        3: "Masukkan NPWP anda",
        4: "Masukkan NIB anda",
        5: "Masukkan Curl anda saat terjadi keluhan"
    }
    return pertanyaan.get(step, "Data antum sudah tercatat, jazakallahu khairan!")

# Fungsi ambil input box (support multi bahasa)
def get_input_box():
    try:
        return driver.find_element(By.XPATH, '//footer//div[@role="textbox"]')
    except NoSuchElementException:
        return None
    
# Fungsi tutup popup modal (kalau ada overlay yang nutup chat)
def tutup_popup():
    try:
        popup = driver.find_element(By.XPATH, '//div[@data-animate-modal-popup="true"]')
        if popup.is_displayed():
            close_btn = driver.find_element(By.XPATH, '//button[@aria-label="Tutup"]')
            close_btn.click()
            print("Popup modal ditutup otomatis")
    except NoSuchElementException:
        pass

# Loop utama
while True:
    try:
        # ambil daftar chat (row = tiap kontak)
        chats = driver.find_elements(By.XPATH, '//div[@role="row"]')

        for chat in chats[:3]:  # cek 3 chat terakhir saja biar ringan
            tutup_popup()  # pastikan popup ketutup dulu
            chat.click()
            time.sleep(2)

            # ambil pesan terakhir
            msgs = driver.find_elements(By.XPATH, '//div[contains(@class,"message-in")]//span[@dir="ltr"]')
            if not msgs:
                continue
            last_msg = msgs[-1].text.strip()
            print("Pesan terakhir:", last_msg)

            # pakai nama chat sebagai ID session
            nama = driver.find_element(By.XPATH, '//header//span[@dir="auto"]').text

            if nama not in sessions:
                sessions[nama] = {"step": 0, "data": {}}

            session = sessions[nama]

            # kalau user ketik "daftar"
            if last_msg.lower() == "daftar":
                session["step"] = 1
                box = get_input_box()
                if box:
                    box.send_keys(tanya(1) + Keys.ENTER)
                continue

            # kalau lagi dalam proses tanya-jawab
            if session["step"] > 0 and session["step"] < 12:
                step = session["step"]
                session["data"][step] = last_msg
                session["step"] += 1

                box = get_input_box()
                if box:
                    box.send_keys(tanya(session["step"]) + Keys.ENTER)

            elif session["step"] == 12:
                session["data"][12] = last_msg
                session["step"] = 99
                hasil = "\n".join([f"{k}: {v}" for k, v in session["data"].items()])
                box = get_input_box()
                if box:
                    box.send_keys("Data antum tersimpan:\n" + hasil + Keys.ENTER)

        time.sleep(5)

    except Exception as e:
        print("Error:", e)
        time.sleep(5)
