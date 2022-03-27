import os
PRO_PATH = os.path.dirname(os.path.abspath(__file__))

class RunConfig:
    """
    运行测试配置
    """
    # 运行测试用例的目录或文件
    cases_path = os.path.join(PRO_PATH, "testcases")

    # 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)。
    driver_type = "chrome-headless"

    # 失败重跑次数
    rerun = "1"

    # 当达到最大失败数，停止执行
    max_fail = "5"

    # 浏览器驱动
    driver = './chromedriver.exe'

    # 报告路径
    NEW_REPORT = "output"

    # browsermod Proxy
    # browsermob_proxy = "E:\githubstore\LAN-autotest-webium\\networking\BrowsermobProxyDist\\browsermob-proxy"
    # browsermob_proxy_port = 8889