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
from config import RunConfig

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def init_env(new_report):
    """
    初始化测试报告目录
    """
    os.mkdir(new_report)
    os.mkdir(new_report + "/image")

# Note: 2021-08-27
#   TODO: Update to 'MAC' and 'URL' mode

def run():
    logger.info("回归模式，开始执行！")
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
    init_env(RunConfig.NEW_REPORT)
    html_report = os.path.join(RunConfig.NEW_REPORT, "report.html")
    xml_report = os.path.join(RunConfig.NEW_REPORT, "junit-xml.xml")
    # suite_name = "test_Baidu.py::TestBaidu::test_Baidu_Main"
    suite_name = "test_GRP261x_Context.py::TestGrp261x"
    # pytest.main(["-s", "-v", os.path.join( RunConfig.cases_path, suite_name ),
    #                 "--html=" + html_report,
    #                 '--metadata-from-json={"name": "admin", "passwd": "123", "base_url": "192.168.92.3"}',
    #                 "--junit-xml=" + xml_report,
    #                 "--self-contained-html"])
    pytest.main(["-v", "-s", os.path.join( RunConfig.cases_path, suite_name ), '--metadata-from-json={"name": "admin", "passwd": "123", "base_url": "http://192.168.92.20/"}', '--count=2'])
    pytest.main(["-v", "-s", os.path.join( RunConfig.cases_path, suite_name ), '--metadata-from-json={"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}', '--count=2'])
    logger.info("运行结束，生成测试报告！")

if __name__ == "__main__":
    run()
