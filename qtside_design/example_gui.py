# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'example_gui.ui'
#
# Created: Wed Aug 24 13:28:12 2016
#      by: PySide6 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader


def _fromUtf8(s):
    return s

try:
    _encoding = QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(423, 298)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.workButton = QPushButton(self.centralwidget)
        self.workButton.setGeometry(QRect(20, 40, 75, 23))
        self.workButton.setObjectName(_fromUtf8("workButton"))
        self.eatButton = QPushButton(self.centralwidget)
        self.eatButton.setGeometry(QRect(20, 80, 75, 23))
        self.eatButton.setObjectName(_fromUtf8("eatButton"))
        self.sleepButton = QPushButton(self.centralwidget)
        self.sleepButton.setGeometry(QRect(20, 120, 75, 23))
        self.sleepButton.setObjectName(_fromUtf8("sleepButton"))
        self.work_progressBar = QProgressBar(self.centralwidget)
        self.work_progressBar.setGeometry(QRect(120, 40, 261, 23))
        self.work_progressBar.setProperty("value", 24)
        self.work_progressBar.setObjectName(_fromUtf8("work_progressBar"))
        self.eat_progressBar = QProgressBar(self.centralwidget)
        self.eat_progressBar.setGeometry(QRect(120, 80, 261, 23))
        self.eat_progressBar.setProperty("value", 24)
        self.eat_progressBar.setObjectName(_fromUtf8("eat_progressBar"))
        self.sleep_progressBar = QProgressBar(self.centralwidget)
        self.sleep_progressBar.setGeometry(QRect(120, 120, 261, 23))
        self.sleep_progressBar.setProperty("value", 24)
        self.sleep_progressBar.setObjectName(_fromUtf8("sleep_progressBar"))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setGeometry(QRect(0, 0, 423, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "QtDesigner_Test", None))
        self.workButton.setText(_translate("MainWindow", "work", None))
        self.eatButton.setText(_translate("MainWindow", "eat", None))
        self.sleepButton.setText(_translate("MainWindow", "sleep", None))


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())