# This Python file uses the following encoding: utf-8

import sys
import time

import os
import logging
import pytest
from conftest import REPORT_DIR
from config import RunConfig
from wpoium import setupUi

import PySide6
dirname = os.path.dirname(PySide6.__file__)
plugin_path = os.path.join(dirname, 'plugins', 'platforms')
os.environ['QT_QPA_PLATFORM_PLUGIN_PATH'] = plugin_path

from PySide6.QtWidgets import QApplication
from PySide6.QtCore import QObject, Signal, Slot, QThread

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)


"""
初始化测试报告目录
"""

# thread
if __name__ == "__main__":
    logger.info("回归模式，开始执行！")

    RunConfig.report_dir = REPORT_DIR
    
    app = QApplication()
    mainUI = setupUi(RunConfig)
    mainUI.main.show()
    sys.exit(app.exec())
