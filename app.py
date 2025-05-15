import time
import threading
import requests
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

# تنظیمات Flask برای سرور وب
app = Flask(__name__)

@app.route('/ping')
def ping():
    return "OK"

# تنظیمات مرورگر
chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_options.add_argument("--log-level=3")

# لیست سایت‌ها به ترتیب
sites = [
    "https://web-chat-mbai.onrender.com/",
    "https://django-1-46yo.onrender.com/"
]

# URL سرویس شما در Render (بعد از دیپلوی پر کنید)
SELF_URL = "https://my-render-app-vkf8.onrender.com//ping"  # این را با URL واقعی جایگزین کنید

def open_and_close_site(site):
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    try:
        driver.get(site)
        print(f"سایت {site} باز شد")
        time.sleep(30)
    except Exception as e:
        print(f"خطا در باز کردن سایت {site}: {e}")
    finally:
        driver.quit()
        print(f"سایت {site} بسته شد")

def self_ping():
    while True:
        try:
            response = requests.get(SELF_URL)
            print(f"Self-ping به {SELF_URL}: وضعیت {response.status_code}")
        except Exception as e:
            print(f"خطا در self-ping: {e}")
        time.sleep(600)  # هر 10 دقیقه

# اجرای سرور Flask و self-ping در نخ‌های جداگانه
if __name__ == "__main__":
    # شروع نخ برای self-ping
    ping_thread = threading.Thread(target=self_ping)
    ping_thread.daemon = True
    ping_thread.start()
    
    # شروع سرور Flask در نخ جداگانه
    flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080))
    flask_thread.daemon = True
    flask_thread.start()
    
    # حلقه اصلی برای سایت‌ها
    while True:
        for site in sites:
            open_and_close_site(site)
            time.sleep(10)