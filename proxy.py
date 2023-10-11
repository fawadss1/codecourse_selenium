from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType


def get_proxies():
    with open('proxy-list.txt', 'r') as file:
        proxies = file.readlines()
    return [proxy.strip() for proxy in proxies]


def rotate_proxy(driver, proxies):
    if not proxies:
        print("All proxies used up.")
        return
    proxy = proxies.pop(0)
    print("Using proxy:", proxy)

    # Set up the proxy for the driver
    proxy_obj = Proxy()
    proxy_obj.proxy_type = ProxyType.MANUAL
    proxy_obj.http_proxy = proxy
    proxy_obj.ssl_proxy = proxy

    # Create a new driver with the rotated proxy
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    driver.quit()
    return webdriver.Chrome(options=options)


# Read the list of proxies from the text file
proxies = get_proxies()

# Set up the initial driver with the first proxy
driver = webdriver.Chrome()
driver = rotate_proxy(driver, proxies)

# Use the driver with the rotated proxy
# Your scraping code goes here

# Rotate the proxy and use the driver again
driver = rotate_proxy(driver, proxies)

# Write the updated list of proxies back to the file
with open('proxy-list.txt', 'w') as file:
    file.write('\n'.join(proxies))
