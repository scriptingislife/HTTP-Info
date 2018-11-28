#
# HTTP Info
#
# Use Selenium and BrowserMob Proxy to get information about a URL.
# - Logs HTTP requests
# - Takes a screenshot
#
# Author: Nathaniel Beckstead <scriptingis.life>
#


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from browsermobproxy import Server
import argparse
import hashlib
import requests
import os


def request_hash(url):
    sha256 = hashlib.sha256()
    resp = requests.get(url)
    if resp.status_code == 200:
        sha256.update(resp.content)
        return sha256.hexdigest()
    else:
        return "None"

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="The URL to retrieve.")
    args = parser.parse_args()

    URL = args.url    
    IMG_OUT = "info/screenshot.png"
    CSV_OUT = "info/http-info.csv"


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

    # Launch Selenium
    print('GET {}'.format(URL))
    driver.get(URL)
    print('Saving screenshot.')
    try:
        screenshot = driver.save_screenshot(IMG_OUT)
    except:
        print("Failed to grab screenshot.")
        screenshot = None

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
        SHA256 Sum: {}
    """

    csv_string = "Request URL, Request Method, Response Status, Response Size, Content Type, SHA256 Sum\n"
    with open(CSV_OUT, 'w') as f:
        f.write(csv_string)
        for entry in network_traffic['log']['entries']:
            entry_hash = request_hash(entry['request']['url'])
            csv_row = ",".join([entry['request']['url'],
                                entry['request']['method'],
                                str(entry['response']['status']),
                                str(entry['response']['bodySize']),
                                entry['response']['content']['mimeType'],
                                entry_hash])
            f.write(csv_row + '\n')
            entry_string = ntw_string.format(entry['request']['url'],
                                            entry['request']['method'],
                                            entry['response']['status'], 
                                            entry['response']['bodySize'], 
                                            entry['response']['content']['mimeType'], 
                                            entry_hash)
            print(entry_string)


if __name__ == '__main__':
    main()
