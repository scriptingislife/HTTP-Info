#
# Use Selenium to grab a screenshot of a website without a GUI.
#
# Required:
# Chromedriver: https://chromedriver.storage.googleapis.com/index.html?path=2.35/
# Selenium module: pip install selenium
#

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
import pprint
import puush
import os

ACCOUNT = puush.Account(os.environ['HTTPINFO_PUUSHAPI'])
DRIVER = 'chromedriver'
WINDOW_SIZE = "1920,1080"

# Create proxy
server = Server(os.environ['HTTPINFO_BMP_PATH'])
server.start()
proxy = server.create_proxy()

# Set Chrome configuration
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--proxy-server={}'.format(proxy.proxy))
chrome_options.add_argument('--ignore-certificate-errors')
chrome_options.add_argument('--disable-web-security')
chrome_options.add_argument('--allow-running-insecure-content')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument("--window-size={}".format(WINDOW_SIZE))

chrome_capabilities = DesiredCapabilities.CHROME.copy()
chrome_capabilities['acceptSslCerts'] = True
chrome_capabilities['acceptInsecureCerts'] = True

proxy.new_har('http-info')
driver = webdriver.Chrome(DRIVER, chrome_options=chrome_options, desired_capabilities=chrome_capabilities)

# Specify URL
URL = str(os.environ['HTTPINFO_URL'])
OUT = "http-info.png"

# Launch Selenium
driver.get(URL)
screenshot = driver.save_screenshot(OUT)

upload = ACCOUNT.upload(OUT)
print(upload.url)

network_traffic = proxy.har
server.stop()

driver.quit()

pp = pprint.PrettyPrinter(indent=2)
pp.pprint(network_traffic)
