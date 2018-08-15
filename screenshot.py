#
# Use Selenium to grab a screenshot of a website without a GUI.
#
# Required:
# Chromedriver: https://chromedriver.storage.googleapis.com/index.html?path=2.35/
# Selenium module: pip install selenium
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

import puush
import os

ACCOUNT = puush.Account("3BF5BF92BC493F6AC7713D2F92869C53")
DRIVER = 'chromedriver'
WINDOW_SIZE = "1920,1080"

# Set headless mode
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size={}".format(WINDOW_SIZE))

driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options)

# Specify URL
URL = str(os.environ['HTTPINFO_URL'])
OUT = "http-info.png"

# Launch Selenium
driver.get(URL)
screenshot = driver.save_screenshot(OUT)

upload = ACCOUNT.upload(OUT)
print(upload.url)

driver.quit()

