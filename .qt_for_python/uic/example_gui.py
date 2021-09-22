# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'example_gui.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(423, 298)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.workButton = QPushButton(self.centralwidget)
        self.workButton.setObjectName(u"workButton")
        self.workButton.setGeometry(QRect(20, 40, 75, 23))
        self.eatButton = QPushButton(self.centralwidget)
        self.eatButton.setObjectName(u"eatButton")
        self.eatButton.setGeometry(QRect(20, 80, 75, 23))
        self.sleepButton = QPushButton(self.centralwidget)
        self.sleepButton.setObjectName(u"sleepButton")
        self.sleepButton.setGeometry(QRect(20, 120, 75, 23))
        self.work_progressBar = QProgressBar(self.centralwidget)
        self.work_progressBar.setObjectName(u"work_progressBar")
        self.work_progressBar.setGeometry(QRect(120, 40, 261, 23))
        self.work_progressBar.setValue(24)
        self.eat_progressBar = QProgressBar(self.centralwidget)
        self.eat_progressBar.setObjectName(u"eat_progressBar")
        self.eat_progressBar.setGeometry(QRect(120, 80, 261, 23))
        self.eat_progressBar.setValue(24)
        self.sleep_progressBar = QProgressBar(self.centralwidget)
        self.sleep_progressBar.setObjectName(u"sleep_progressBar")
        self.sleep_progressBar.setGeometry(QRect(120, 120, 261, 23))
        self.sleep_progressBar.setValue(24)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 423, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QtDesigner_Test", None))
        self.workButton.setText(QCoreApplication.translate("MainWindow", u"work", None))
        self.eatButton.setText(QCoreApplication.translate("MainWindow", u"eat", None))
        self.sleepButton.setText(QCoreApplication.translate("MainWindow", u"sleep", None))
    # retranslateUi

