import time
import threading
import requests
from flask import Flask
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

# لیست سایت‌ها (شامل آدرس جدید)
sites = [
    "https://web-chat-dgbt.onrender.com/",
    "https://django-1-46yo.onrender.com/",
    "https://c-drive.onrender.com/"
]

# آدرس URL سرویس شما در Render (حتماً بعد از دیپلوی آدرس درست را جایگزین کن)
SELF_URL = "https://my-render-app-vkf8.onrender.com/ping"

def ping_site(site):
    try:
        response = requests.get(site, timeout=10)
        logger.info(f"Pinged {site}: Status {response.status_code}")
    except Exception as e:
        logger.error(f"Error pinging {site}: {e}")

def self_ping():
    time.sleep(60)  # صبر 1 دقیقه تا سرور Flask راه‌اندازی بشه
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

        # شروع سرور Flask
        flask_thread = threading.Thread(target=lambda: app.run(host="0.0.0.0", port=8000, use_reloader=False))
        flask_thread.daemon = True
        flask_thread.start()

        # حلقه اصلی برای پینگ سایت‌ها
        logger.info("Starting main loop for sites")
        while True:
            for site in sites:
                ping_site(site)
                time.sleep(15)  # 15 ثانیه بین هر پینگ سایت
            time.sleep(5)  # 5 ثانیه تأخیر بعد از هر چرخه کامل
    except Exception as e:
        logger.error(f"Main loop error: {e}")
