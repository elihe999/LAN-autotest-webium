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
from wpoium import setupUi

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

def run():
    logger.info("回归模式，开始执行！")
    now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
    RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
    init_env(RunConfig.NEW_REPORT)
    html_report = os.path.join(RunConfig.NEW_REPORT, "report.html")
    xml_report = os.path.join(RunConfig.NEW_REPORT, "junit-xml.xml")
    suite_name = "test_GRP261x_Factory.py"
    pytest.main(["-v", "-s", os.path.join( RunConfig.cases_path, suite_name ), '--metadata-from-json={"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}', '--count=1', '--repeat-scope=session', "--self-contained-html", "--html=" + html_report, "--maxfail", RunConfig.max_fail])
    logger.info("运行结束，生成测试报告！")

# thread
class ExecPyTestCase(QThread):
    mySignal = Signal(str, str)
    def __init__(self): 
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    # custom method
    def init_env(self, new_report):
        """
        初始化测试报告目录
        """
        os.mkdir(new_report)
        os.mkdir(new_report + "/image")

    @Slot(str, str)
    def run(self, case_name, params):
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        RunConfig.NEW_REPORT = os.path.join(REPORT_DIR, now_time)
        self.init_env(RunConfig.NEW_REPORT)
        html_report = os.path.join(RunConfig.NEW_REPORT, "report.html")
        xml_report = os.path.join(RunConfig.NEW_REPORT, "junit-xml.xml")
        suite_name = case_name
        pytest.main(["-v", "-s", os.path.join( RunConfig.cases_path, suite_name ), '--metadata-from-json={"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}', '--count=1', '--repeat-scope=session', "--self-contained-html", "--html=" + html_report, "--maxfail", RunConfig.max_fail])
        # self.mySignal.emit("test", "test")

if __name__ == "__main__":

    app = QApplication()
    mainUI = setupUi(RunConfig)
    pytestExec = ExecPyTestCase()
    mainUI.sendsignal.connect(pytestExec.run)
    mainUI.main.show()
    sys.exit( app.exec_() )
