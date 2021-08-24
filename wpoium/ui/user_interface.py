# -*- coding: utf-8 -*-

"""
@author:  Eli
@data: 2021-08-18
@function pytest UI
"""
import time
from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QEnum, QFlag, QObject, Qt, Signal, Slot, QThread
# WARNING:root:qt_material must be imported after PySide or PyQt!
from qt_material import QtStyleTools
import os
import json

from wpoium.ui.worker import BackgroundWorker


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    sendsignal = Signal(str, str, str, str, str)

    def __init__(self):
        """SETUP UI"""
        super().__init__()
        self.main = QUiLoader().load('wpoium/ui/autotest_wig.ui', self)
        self.main.testSuiteList.clicked.connect(self.changeItem)
        self.main.pushButtonStart.clicked.connect(self.checkParamVaild)
        self.main.pushButtonStop.clicked.connect(self.stopTest)

        ### BACKGROUND WORKER ###
        self.background_worker_thread_ = QThread()
        self.background_worker_ = BackgroundWorker()
        self.background_worker_.moveToThread(self.background_worker_thread_)
        ###  CONNECT ###
        self.sendsignal.connect(self.background_worker_.run)
        self.background_worker_.report_progress.connect(self.showResult)

        ################################################################
        self.apply_stylesheet(self.main, 'light_blue.xml')
        self.main.actionDark_Blue.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'dark_teal.xml'))
        self.main.actionLight_Blue.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_blue.xml'))
        self.main.actionLight_Cyan.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_cyan.xml'))
        self.main.actionLight_Pink.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_pink.xml'))

        # ============================================
        # variable
        # ============================================
        self.suite_name = ""
        self.config = None
        # ============================================
        # END INIT
        # ============================================

    ######          function        ######
    def readSuiteFolder(self, suite_path):
        """
        Load test case on list view
        """
        configd = False
        if os.path.exists(suite_path):
            files = os.listdir(suite_path)
            for file in files:
                file_path = os.path.join(suite_path, file)
                if os.path.isfile(file_path) and file.startswith('test'):
                    # test_  [  ]  .py
                    item_name = file[5:-3]
                    item = QListWidgetItem(item_name, self.main.testSuiteList)
                    if not configd:
                        self.main.testSuiteList.setCurrentItem(item)
                        configd = True

    def changeItem(self):
        """
        Check input
        """
        selected_item_name = ""
        selected_item_name = self.main.testSuiteList.selectedItems()[0].text()
        self.changeSeletedCase(selected_item_name)

    def checkParamVaild(self):
        if self.suite_name != "":
            print(self.main.macLineEdit.text())
            print(self.main.userNameLineEdit.text())
            print(self.main.passwdLineEdit.text())
            print(self.main.spinBoxLoop.value())
            print(self.main.spinBoxTime.value())
            mac_addr = self.main.macLineEdit.text()
            user_name = self.main.userNameLineEdit.text()
            password = self.main.passwdLineEdit.text()
            loop_num = self.main.spinBoxLoop.value()
            sleep_time = self.main.spinBoxTime.value()
            if len(mac_addr) == 0 or len(user_name) == 0 or len(password) == 0:
                print("Param is empty")
                return
            _j_base_metas = {"name": user_name,
                 "passwd": password,
                 "mac": mac_addr}
            base_meta = json.dumps(_j_base_metas)
            if not self.background_worker_thread_.isRunning():
                self.background_worker_thread_.start()
            print("OK")
            # {"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}
            self.sendsignal.emit(os.path.join(self.config.cases_path, self.suite_name),
                                 self.config.html_report, base_meta, sleep_time, loop_num)

    def changeSeletedCase(self, case_name):
        self.suite_name = "test_"+case_name+".py"

    def stopTest(self):
        self.background_worker_thread_.stop()

    ######          SOLT            ######
    @Slot()
    def showResult(self, test):
        print(test)


def setupUi(config):
    # frame
    frame = RuntimeStylesheets()
    frame.config = config
    frame.readSuiteFolder(config.cases_path)
    return frame


# main test
if __name__ == "__main__":
    app = QApplication()

    # Local file
    QFontDatabase.addApplicationFont(os.path.join(
        'font', 'JiZiJingDianFangSongJianFan-Shan-2.ttf'))

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()
