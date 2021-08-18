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
#WARNING:root:qt_material must be imported after PySide or PyQt!
from qt_material import QtStyleTools

import os

class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('wpoium/ui/autotest_wig.ui', self)
        self.apply_stylesheet(self.main, 'light_blue.xml')
        self.main.actionDark_Blue.triggered.connect(lambda: self.apply_stylesheet(self.main, 'dark_teal.xml'))
        self.main.actionLight_Blue.triggered.connect(lambda: self.apply_stylesheet(self.main, 'light_blue.xml'))
        self.main.actionLight_Cyan.triggered.connect(lambda: self.apply_stylesheet(self.main, 'light_cyan.xml'))
        self.main.actionLight_Pink.triggered.connect(lambda: self.apply_stylesheet(self.main, 'light_pink.xml'))
        self.main.testSuiteList.clicked.connect(self.checkParamVaild)

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
                    print(file)
                    # test_  [  ]  .py
                    item_name = file[5:-3]
                    item = QListWidgetItem(item_name, self.main.testSuiteList)
                    if not configd:
                        self.main.testSuiteList.setCurrentItem(item)
                        configd = True

    def checkParamVaild(self):
        """
        Check input
        """
        selected_item_name = ""
        selected_item_name = self.main.testSuiteList.selectedItems()[0].text()
        self.changeSeletedCase( selected_item_name )

    def changeSeletedCase(self, case_name):
        print( case_name )

def setupUi():
    # frame
    frame = RuntimeStylesheets()
    frame.readSuiteFolder("testcases")
    return frame

# main test
if __name__ == "__main__":
    app = QApplication()

    # Local file
    QFontDatabase.addApplicationFont(os.path.join('font','JiZiJingDianFangSongJianFan-Shan-2.ttf'))

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()