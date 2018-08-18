#
# HTTP Info
#
# Use Selenium and BrowserMob Proxy to get information about a URL.
# - Logs HTTP requests
# - Uploads a screenshot to puush.me
#
# Author: Nathaniel Beckstead <scriptingis.life>
#


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
import puush
import os


def main():
    PUUSH_API = os.getenv('HTTPINFO_PUUSHAPI')
    if PUUSH_API:
        ACCOUNT = puush.Account(PUUSH_API)
    else:
        ACCOUNT = None
    DRIVER = 'chromedriver'
    WINDOW_SIZE = "1920,1080"

    print('Setting up Selenium environment.')

    # Create proxy
    server = Server(os.getenv('HTTPINFO_BMP_PATH'))
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
    try:
        URL = os.getenv('HTTPINFO_URL')
    except KeyError:
        return 1
    OUT = "http-info.png"

    # Launch Selenium
    print('GET {}'.format(URL))
    driver.get(URL)
    print('Saving screenshot.')
    try:
        screenshot = driver.save_screenshot(OUT)
    except:
        print("Failed to grab screenshot.")
        screenshot = None

    if screenshot:
        print('Uploading screenshot.')
        if ACCOUNT is not None:
            upload = ACCOUNT.upload(OUT)
            print(upload.url)

    # JSON blob of HTTP requests
    network_traffic = proxy.har

    server.stop()
    driver.quit()

    ntw_string = """
        Request URL: {}
        Request Method: {}
        Response Status: {}
        Reponse Size: {}
        Content Type: {}
    """

    for entry in network_traffic['log']['entries']:
        entry_string = ntw_string.format(entry['request']['url'], entry['request']['method'], entry['response']['status'], entry['response']['bodySize'], entry['response']['content']['mimeType'])
        print(entry_string)


if __name__ == '__main__':
    main()