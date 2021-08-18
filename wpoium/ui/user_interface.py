# -*- coding: utf-8 -*-

"""
@author:  Eli
@data: 2021-08-18
@function pytest UI
"""

from PySide6.QtWidgets import QApplication, QMainWindow, QListWidgetItem
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QEnum, QFlag, QObject, Qt
# WARNING:root:qt_material must be imported after PySide or PyQt!
from qt_material import QtStyleTools
import pytest
import os


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
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
            pytest.main(["-v", "-s", os.path.join(self.config.cases_path, self.suite_name),
                     '--metadata-from-json={"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}'])

    def changeSeletedCase(self, case_name):
        self.suite_name = "test_"+case_name+".py"
        print( self.suite_name )


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
