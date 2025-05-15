import time
import threading
import requests
from flask import Flask
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import logging

# تنظیمات لاگ
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# تنظیمات Flask برای سرور وب
app = Flask(__name__)

@app.route('/ping')
def ping():
    logger.info("Received ping request")
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

# URL سرویس شما در Render
SELF_URL = "https://my-render-app-vkf8.onrender.com/ping"  # این باید URL واقعی سرویس شما باشه

def open_and_close_site(site):
    try:
        service = Service(ChromeDriverManager().install())
        driver = webdriver.Chrome(service=service, options=chrome_options)
        logger.info(f"Opening site: {site}")
        driver.get(site)
        time.sleep(30)
        logger.info(f"Site {site} opened successfully")
    except Exception as e:
        logger.error(f"Error opening site {site}: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()
            logger.info(f"Site {site} closed")

def self_ping():
    time.sleep(60)  # صبر 1 دقیقه تا سرور Flask کامل راه‌اندازی بشه
    while True:
        try:
            response = requests.get(SELF_URL, timeout=10)
            logger.info(f"Self-ping to {SELF_URL}: Status {response.status_code}")
        except Exception as e:
            logger.error(f"Self-ping error: {e}")
        time.sleep(600)  # هر 10 دقیقه

# اجرای سرور Flask و self-ping در نخ‌های جداگانه
if __name__ == "__main__":
    try:
        # شروع نخ برای self-ping
        ping_thread = threading.Thread(target=self_ping)
        ping_thread.daemon = True
        ping_thread.start()
        
        # حلقه اصلی برای سایت‌ها
        logger.info("Starting main loop for sites")
        flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8080, use_reloader=False))
        flask_thread.daemon = True
        flask_thread.start()
        
        while True:
            for site in sites:
                open_and_close_site(site)
                time.sleep(10)
    except Exception as e:
        logger.error(f"Main loop error: {e}")