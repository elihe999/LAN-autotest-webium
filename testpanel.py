# This Python file uses the following encoding: utf-8

import sys
import time

import os
import logging
import pytest
from conftest import REPORT_DIR
from config import RunConfig
from wpoium import setupUi

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


def init_env(new_report):
    """
    初始化测试报告目录
    """
    os.mkdir(new_report)
    os.mkdir(new_report + "/image")

def run():
    logger.info("回归模式，开始执行！")
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
    init_env(RunConfig.NEW_REPORT)
    html_report = os.path.join(RunConfig.NEW_REPORT, "report.html")
    xml_report = os.path.join(RunConfig.NEW_REPORT, "junit-xml.xml")
    suite_name = "test_GRP261x_Factory.py"
    pytest.main(["-v", "-s", os.path.join(RunConfig.cases_path, suite_name),
                 '--metadata-from-json={"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}', '--count=1', '--repeat-scope=session', "--self-contained-html", "--html=" + html_report, "--maxfail", RunConfig.max_fail])
    logger.info("运行结束，生成测试报告！")


# thread
if __name__ == "__main__":
    logger.info("回归模式，开始执行！")
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
    RunConfig.html_report = os.path.join(RunConfig.NEW_REPORT, "report.html")
    app = QApplication()
    mainUI = setupUi(RunConfig)
    mainUI.main.show()
    sys.exit(app.exec_())
