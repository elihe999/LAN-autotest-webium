# -*- coding: utf-8 -*-

"""
@author:  Eli
@data: 2021-08-18
@function pytest UI
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QEnum, QFlag, QObject, Qt, Signal, Slot, QThread
# WARNING:root:qt_material must be imported after PySide or PyQt!
from qt_material import QtStyleTools
import pytest
import os

# class Worker(QObject):
#     def __init__(self):
#         QObject.__init__(self)

#     def dowork(self, sender, name, params):
#         sender.emit(name, params)

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

class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    sendsignal = Signal(str, str)
    def __init__(self):
        """"""
        super().__init__(self)
        self.main = QUiLoader().load('wpoium/ui/autotest_wig.ui', self)
        self.apply_stylesheet(self.main, 'light_blue.xml')
        self.main.actionDark_Blue.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'dark_teal.xml'))
        self.main.actionLight_Blue.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_blue.xml'))
        self.main.actionLight_Cyan.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_cyan.xml'))
        self.main.actionLight_Pink.triggered.connect(
            lambda: self.apply_stylesheet(self.main, 'light_pink.xml'))
        self.main.testSuiteList.clicked.connect(self.changeItem)
        self.main.pushButtonStart.clicked.connect(self.checkParamVaild)
        # ============================================
        # variable
        # ============================================
        self.suite_name = ""
        self.config = None
        #=============================================
        # self.thread = QThread()
        # self.worker = Worker()
        # self.worker.moveToThread(self.thread)
        # END INIT
                
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
            # self.worker.dowork( self.sendsignal,
            #                     self.suite_name,
            #                     '{"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}')
            # self.sendsignal.emit(self.suite_name, '{"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}')

    def changeSeletedCase(self, case_name):
        self.suite_name = "test_"+case_name+".py"
        print( self.suite_name )

    @Slot(str, str)
    def showResult(self, casename, params):
        print(casename, params)

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
