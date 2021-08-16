# This Python file uses the following encoding: utf-8
import json
import re
import requests
import sys
import time
import webbrowser
from collections import deque

import os
import logging
import pytest
from conftest import REPORT_DIR


# 配置浏览器驱动类型(chrome/firefox/chrome-headless/firefox-headless)
driver_type = "chrome"

# 浏览器驱动
driver = './chromedriver.exe'

# 报告路径
NEW_REPORT = "output"

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

########
#GLOBAL#
########
G_REPORT_NAME = "output"
PRO_PATH = os.path.dirname(os.path.abspath(__file__))
CASEPATH = os.path.join(PRO_PATH, "testcases")
RunConfig_NEW_REPORT = ""

def run():
    logger.info("回归模式，开始执行！")
    html_report = os.path.join(RunConfig_NEW_REPORT, "report.html")
    xml_report = os.path.join(RunConfig_NEW_REPORT, "junit-xml.xml")
    # suite_name = "test_Baidu.py::TestBaidu::test_Baidu_Main"
    suite_name = "test_GRP261x_Context.py::TestGrp261x"
    pytest.main(["-s", "-v", os.path.join( CASEPATH, suite_name ),
                    "--html=" + html_report,
                    '--metadata-from-json={"name": "admin", "passwd": "123", "base_url": "192.168.92.3"}',
                    "--junit-xml=" + xml_report,
                    "--self-contained-html"])
    logger.info("运行结束，生成测试报告！")

if __name__ == "__main__":
    run()
