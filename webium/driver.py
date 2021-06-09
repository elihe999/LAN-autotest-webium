import webium.settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
_driver_instance = None


def get_driver():
    chromedriver_path = webium.settings.chromedriverpath
    c_service = Service(chromedriver_path)
    c_service.command_line_args()
    c_service.start()
    chrome_options = Options()
    if hasattr(webium.settings, "chrome_nosandbox") and webium.settings.chrome_nosandbox:
        chrome_options.add_argument('--no-sandbox')
    if hasattr(webium.settings, "chrome_disable_shmusage") and webium.settings.chrome_disable_shmusage:
        chrome_options.add_argument('--disable-dev-shm-usage')
    if hasattr(webium.settings, "chrome_ignore_certificate_errors") and webium.settings.chrome_ignore_certificate_errors:
        chrome_options.add_argument('--ignore-certificate-errors')
    if hasattr(webium.settings, "chrome_disable_gpu") and webium.settings.chrome_disable_gpu:
        chrome_options.add_argument('--disable-gpu')
    if hasattr(webium.settings, "chrome_disable_plugins") and webium.settings.chrome_disable_plugins:
        chrome_options.add_argument('--disable-plugins')
    if hasattr(webium.settings, "chrome_handless") and webium.settings.chrome_handless:
        chrome_options.add_argument('--headless')
    
    service_args = []

    if hasattr(webium.settings, "service_load_images") and webium.settings.service_load_images:
        service_args.append('--load-images=yes')
    else:
        service_args.append('--load-images=no')
    
    if hasattr(webium.settings, "service_disk_cache") and webium.settings.service_disk_cache:
        service_args.append('--disk-cache=yes')
    else:
        service_args.append('--disk-cache=no')
    if hasattr(webium.settings, "service_ignore_ssl_errors") and webium.settings.service_ignore_ssl_errors:
        service_args.append('--ignore-ssl-errors=true')
    else:
        service_args.append('--ignore-ssl-errors=false')


    global _driver_instance
    if not _driver_instance:
        _driver_instance = webdriver.Chrome(chrome_options=chrome_options, service_args=service_args,
                                            executable_path=chromedriver_path)
        _driver_instance.implicitly_wait(webium.settings.implicit_timeout)
    return _driver_instance


def get_driver_no_init():
    return _driver_instance


def close_driver():
    global _driver_instance
    if _driver_instance:
        _driver_instance.quit()
        _driver_instance = None
