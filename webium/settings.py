from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By

driver_class = Chrome
implicit_timeout = 30
wait_timeout = 30

chromedriverpath =  r"chromedriver.exe"
chrome_nosandbox = True
chrome_handless = False
chrome_disable_shmusage = True
chrome_disable_gpu = True
chrome_ignore_certificate_errors = True
chrome_disable_plugins = True
service_load_images = False
service_disk_cache = True
service_ignore_ssl_errors = True

default_search_type = By.ID

waitnum = 7
shortwaitnum = 15
middlewaitnum = 35
longwaitnum = 60

try:
    from local_webium_settings import *  # noqa
except ImportError:
    pass
