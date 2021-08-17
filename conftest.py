import os
import pytest
from py.xml import html
from selenium import webdriver
from selenium.webdriver import Remote
from selenium.webdriver.chrome.options import Options as CH_Options
from selenium.webdriver.firefox.options import Options as FF_Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from config import RunConfig

# 项目目录配置
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
REPORT_DIR = BASE_DIR + "/output/"
proxy = None

# 定义基本测试环境
# @pytest.fixture(scope="function")
# def base_url():
#     return RunConfig.url


# 设置用例描述表头
def pytest_html_results_table_header(cells):
    cells.insert(2, html.th("Description"))
    cells.pop()


# 设置用例描述表格
def pytest_html_results_table_row(report, cells):
    if hasattr(report, "description"):
        cells.insert(2, html.td(report.description))
        cells.pop()

def pytest_configure(config):
    # 添加接口地址与项目名称
    config._metadata["项目名称"] = "GSATE Web UI"
    # 删除Java_Home
    # config._metadata.pop("JAVA_HOME")

@pytest.mark.optionalhook
def pytest_html_results_summary(prefix):
    prefix.extend([html.p("Auto Test Version: 0.0.1 Preview")])
    prefix.extend([html.p("Test Suite Version: VOIP R&S Team")])

@pytest.mark.hookwrapper
def pytest_runtest_makereport(item):
    """
    用于向测试用例中添加用例的开始时间、内部注释，和失败截图等.
    :param item:
    """
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()
    report.description = description_html(item.function.__doc__)
    report.nodeid = report.nodeid.encode("utf-8").decode("unicode_escape")
    extra = getattr(report, "extra", [])
    if report.when == "call" or report.when == "setup":
        xfail = hasattr(report, "wasxfail")
        if (report.skipped and xfail) or (report.failed and not xfail):
            case_path = report.nodeid.replace("::", "_") + ".png"
            if "[" in case_path:
                case_name = case_path.split("-")[0] + "].png"
            else:
                case_name = case_path
            capture_screenshots(case_name)
            img_path = "image/" + case_name.split("/")[-1]
            if img_path:
                html = '<div><img src="%s" alt="screenshot" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % img_path
                extra.append(pytest_html.extras.html(html))
        report.extra = extra
    # import json
    # global proxy
    # proxy.wait_for_traffic_to_stop(1, 60)
    # # 保存har中的信息到本地
    # with open("1.har", "w",encoding="utf-8") as outfile:
    #     json.dump(proxy.har, outfile,indent=2,ensure_ascii=False)


def description_html(desc):
    """
    将用例中的描述转成HTML对象
    :param desc: 描述
    :return:
    """
    if desc is None:
        return "No case description"
    desc_ = ""
    for i in range(len(desc)):
        if i == 0:
            pass
        elif desc[i] == "\n":
            desc_ = desc_ + ";"
        else:
            desc_ = desc_ + desc[i]
    
    desc_lines = desc_.split(";")
    desc_html = html.html(
        html.head(
            html.meta(name="Content-Type", value="text/html; charset=latin1")),
        html.body(
            [html.p(line) for line in desc_lines]))
    return desc_html


def capture_screenshots(case_name):
    """
    配置用例失败截图路径
    :param case_name: 用例名
    :return:
    """
    global driver
    file_name = case_name.split("/")[-1]
    if RunConfig.NEW_REPORT is None:
        raise NameError("没有初始化测试报告目录")
    else:
        image_dir = os.path.join(RunConfig.NEW_REPORT, "image", file_name)
        if RunConfig.driver is not None:
            try:
                RunConfig.driver.save_screenshot(image_dir)
            except BaseException:
                pass


# 启动浏览器
@pytest.fixture(scope="session", autouse=True)
def browser():
    """
    全局定义浏览器驱动
    :return:
    """
    global driver
    global proxy

    if RunConfig.driver_type == "chrome":
        # 本地chrome浏览器
        driver = webdriver.Chrome()
        driver.maximize_window()

    elif RunConfig.driver_type == "firefox":
        # 本地firefox浏览器
        driver = webdriver.Firefox()
        driver.maximize_window()

    elif RunConfig.driver_type == "chrome-headless":
        # chrome headless模式
        chrome_options = CH_Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")

        if hasattr(RunConfig, "browsermob_proxy"):
            # browsermobproxy
            from browsermobproxy import Server
            opt_dict={"port":8888}
            if hasattr(RunConfig, "browsermob_proxy"):
                opt_dict={"port":RunConfig.browsermob_proxy_port}
            server = Server(path=RunConfig.browsermob_proxy, options=opt_dict)
            server.start()
            proxy = server.create_proxy()
            chrome_options.add_argument("--proxy-server={0}".format(proxy.proxy))
        if hasattr(RunConfig, "chrome_disable_plugins"):
            chrome_options.add_argument("--disable-plugins")
        if hasattr(RunConfig, "chrome_nosandbox"):
            chrome_options.add_argument("--no-sandbox")
        if hasattr(RunConfig, "chrome_disable_shmusage"):
            chrome_options.add_argument("--disable-dev-shm-usage")
        if hasattr(RunConfig, "chrome_ignore_certificate_errors"):
            chrome_options.add_argument("--ignore-certificate-errors")
        if hasattr(RunConfig, "chrome_disable_gpu"):
            chrome_options.add_argument("--disable-gpu")
        if hasattr(RunConfig, "chrome_disable_plugins"):
            chrome_options.add_argument("--disable-plugins")
        # chrome_options.add_argument("--window-size=1920x1080")
        # service
        service_args = []
        if hasattr(RunConfig, "service_load_images"):
            service_args.append("--load-images=yes")
        else:
            service_args.append("--load-images=no")
        if hasattr(RunConfig, "service_disk_cache"):
            service_args.append("--disk-cache=yes")
        else:
            service_args.append("--disk-cache=no")
        if hasattr(RunConfig, "service_ignore_ssl_errors"):
            service_args.append("--ignore-ssl-errors=true")
        else:
            service_args.append("--ignore-ssl-errors=false")
        # 必须有这一句，才能在后面获取到performance

        chrome_options.add_experimental_option("w3c", False)
        caps = DesiredCapabilities.CHROME
        caps["loggingPrefs"] = {"performance": "ALL"}
        # caps["goog:loggingPrefs"] = {"browswer": "ALL"}
        driver = webdriver.Chrome(options=chrome_options, service_args=service_args, desired_capabilities=caps)
        # proxy.new_har("test", options={"captureContent": True, "captureHeaders": True})     # 开启代理监控，如果不监控会拿不到请求内容

    elif RunConfig.driver_type == "firefox-headless":
        # firefox headless模式
        firefox_options = FF_Options()
        firefox_options.headless = True
        driver = webdriver.Firefox(firefox_options=firefox_options)

    elif RunConfig.driver_type == "grid":
        # 通过远程节点运行
        driver = Remote(command_executor="http://localhost:4444/wd/hub",
                        desired_capabilities={
                              "browserName": "chrome",
                        })
        driver.set_window_size(1920, 1080)

    else:
        raise NameError("driver驱动类型定义错误！")

    RunConfig.driver = driver

    return driver


# 关闭浏览器
@pytest.fixture(scope="session", autouse=True)
def browser_close():
    yield driver
    driver.quit()
    print("test end!")

if __name__ == "__main__":
    capture_screenshots("test_dir/test_baidu_search.test_search_python.png")
