# -*- coding: utf-8 -*-

"""
@author:  Eli
@data: 2021-08-18
@function pytest UI
"""

from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from PySide6.QtCore import QStringListModel
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

    def readSuiteFolder(self, suite_path):
        """
        Load test case on list view
        """
        model = QStringListModel()
        name_list = []
        if os.path.exists(suite_path):
            files = os.listdir(suite_path)
            for file in files:
                file_path = os.path.join(suite_path, file)
                if os.path.isfile(file_path) and file.startswith('test'):
                    print(file)
                    name_list.append(file)
        # load model
        model.setStringList(name_list)
        self.main.testSuiteList.setWrapping(False)
        self.main.testSuiteList.setModel(model)

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