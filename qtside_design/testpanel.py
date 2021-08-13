# This Python file uses the following encoding: utf-8
from PySide2.QtCore import QObject, QThread, QTimer, Signal, Slot, QFile, QIODevice, QTextStream, QByteArray
from PySide2.QtWidgets import QAction, QApplication, QCheckBox, QLabel, QComboBox, QLineEdit, QMenu, QPushButton, QRadioButton, QSpinBox, QTextEdit, QWidget, QFileDialog
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
driver_type = "chrome-headless"

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

class Worker(QObject):

    def __init__(self):
        QObject.__init__(self)


class mainWindow(QObject):

    def __init__(self):
        # must init parent QObject,if you want to use signal
        QObject.__init__(self)
        self.widget = QWidget()
        self.ipLabel = QLabel(self.widget)
        self.thread = QThread()
        self.worker = Worker()
        self.passwordLabel = QLabel(self.widget)
        self.startBtn = QPushButton(self.widget)
        #################################################
        # slot
        #################################################
        self.startBtn.clicked.connect(self.run)

    def init_env(self, new_report):
        """
        初始化测试报告目录
        """
        global RunConfig_NEW_REPORT
        # global
        now_time = time.strftime("%Y_%m_%d_%H_%M_%S")
        new_report_dir =  os.path.join(new_report, now_time)
        new_report_img_dir = os.path.join(new_report_dir, 'image')
        import platform
        if platform.system() == 'Windows':
            new_report_dir = new_report_dir.replace('/', "\\")
            new_report_img_dir = new_report_img_dir.replace('/', '\\')
        else:
            new_report_dir = new_report_dir.replace('\\', '/')
            new_report_img_dir = new_report_img_dir.replace('\\', '/')
        RunConfig_NEW_REPORT = new_report_dir
        os.mkdir(new_report_dir)
        os.mkdir(new_report_img_dir)

    def setupUI(self):
        # set text content /value
        self.widget.setWindowTitle("自动重启升降级测试工具")
        self.ipLabel.setText("初始IP:")
        self.startBtn.setText("开始测试")
        self.passwordLabel.setText("密码:")
        self.widget.show()

    def run(self):
        logger.info("回归模式，开始执行！")
        self.init_env(REPORT_DIR)
        html_report = os.path.join(RunConfig_NEW_REPORT, "report.html")
        xml_report = os.path.join(RunConfig_NEW_REPORT, "junit-xml.xml")
        suite_name = "test_GRP261x_Context.py::TestGrp261x::test_device_login"
        pytest.main(["-s", "-v", os.path.join( CASEPATH, suite_name ),
                     "--html=" + html_report,
                     "--name=" + "test",
                     "--passwd=" + "test",
                     "--base_url=" + "test",
                     "--junit-xml=" + xml_report,
                     "--self-contained-html"])
        logger.info("运行结束，生成测试报告！")

# if __name__ == "__main__":

app = QApplication()
window = mainWindow()
window.setupUI()
sys.exit(app.exec_())
