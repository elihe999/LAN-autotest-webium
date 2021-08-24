# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'autotest_wig.ui'
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
        MainWindow.resize(800, 669)
        sizePolicy = QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.actionAbout = QAction(MainWindow)
        self.actionAbout.setObjectName(u"actionAbout")
        self.actionAboutShow = QAction(MainWindow)
        self.actionAboutShow.setObjectName(u"actionAboutShow")
        self.actionUI_Light_Blue = QAction(MainWindow)
        self.actionUI_Light_Blue.setObjectName(u"actionUI_Light_Blue")
        self.actionDark_Blue = QAction(MainWindow)
        self.actionDark_Blue.setObjectName(u"actionDark_Blue")
        self.actionLight_Blue = QAction(MainWindow)
        self.actionLight_Blue.setObjectName(u"actionLight_Blue")
        self.actionLight_Cyan = QAction(MainWindow)
        self.actionLight_Cyan.setObjectName(u"actionLight_Cyan")
        self.actionLight_Pink = QAction(MainWindow)
        self.actionLight_Pink.setObjectName(u"actionLight_Pink")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.stackedWidget = QStackedWidget(self.centralwidget)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.testSuitePage = QWidget()
        self.testSuitePage.setObjectName(u"testSuitePage")
        self.verticalLayout = QVBoxLayout(self.testSuitePage)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.viewFrame = QFrame(self.testSuitePage)
        self.viewFrame.setObjectName(u"viewFrame")
        self.viewFrame.setStyleSheet(u"border: none;")
        self.viewFrame.setFrameShape(QFrame.StyledPanel)
        self.viewFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.viewFrame)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.testSuiteList = QListWidget(self.viewFrame)
        self.testSuiteList.setObjectName(u"testSuiteList")

        self.verticalLayout_2.addWidget(self.testSuiteList)


        self.verticalLayout.addWidget(self.viewFrame)

        self.controlInputFrame = QFrame(self.testSuitePage)
        self.controlInputFrame.setObjectName(u"controlInputFrame")
        sizePolicy1 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.controlInputFrame.sizePolicy().hasHeightForWidth())
        self.controlInputFrame.setSizePolicy(sizePolicy1)
        self.controlInputFrame.setStyleSheet(u"border: none;")
        self.controlInputFrame.setFrameShape(QFrame.StyledPanel)
        self.controlInputFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.controlInputFrame)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.pushButtonStart = QPushButton(self.controlInputFrame)
        self.pushButtonStart.setObjectName(u"pushButtonStart")

        self.horizontalLayout_4.addWidget(self.pushButtonStart)

        self.pushButtonStop = QPushButton(self.controlInputFrame)
        self.pushButtonStop.setObjectName(u"pushButtonStop")

        self.horizontalLayout_4.addWidget(self.pushButtonStop)


        self.verticalLayout.addWidget(self.controlInputFrame)

        self.stackedWidget.addWidget(self.testSuitePage)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.stackedWidget.addWidget(self.page_2)

        self.horizontalLayout.addWidget(self.stackedWidget)

        self.controlFrame = QFrame(self.centralwidget)
        self.controlFrame.setObjectName(u"controlFrame")
        self.controlFrame.setFrameShape(QFrame.StyledPanel)
        self.controlFrame.setFrameShadow(QFrame.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.controlFrame)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.logBrowser = QTextBrowser(self.controlFrame)
        self.logBrowser.setObjectName(u"logBrowser")
        sizePolicy2 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.logBrowser.sizePolicy().hasHeightForWidth())
        self.logBrowser.setSizePolicy(sizePolicy2)

        self.verticalLayout_3.addWidget(self.logBrowser)

        self.textBrowser = QTextBrowser(self.controlFrame)
        self.textBrowser.setObjectName(u"textBrowser")
        sizePolicy2.setHeightForWidth(self.textBrowser.sizePolicy().hasHeightForWidth())
        self.textBrowser.setSizePolicy(sizePolicy2)
        self.textBrowser.setMaximumSize(QSize(16777215, 22))
        self.textBrowser.setStyleSheet(u"margin:0px;")
        self.textBrowser.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.textBrowser.setSizeAdjustPolicy(QAbstractScrollArea.AdjustToContents)
        self.textBrowser.setTabChangesFocus(False)
        self.textBrowser.setAcceptRichText(False)

        self.verticalLayout_3.addWidget(self.textBrowser)

        self.processFrame = QFrame(self.controlFrame)
        self.processFrame.setObjectName(u"processFrame")
        sizePolicy3 = QSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.processFrame.sizePolicy().hasHeightForWidth())
        self.processFrame.setSizePolicy(sizePolicy3)
        self.processFrame.setMaximumSize(QSize(16777215, 50))
        self.processFrame.setFrameShape(QFrame.StyledPanel)
        self.processFrame.setFrameShadow(QFrame.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.processFrame)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.statusLabel = QLabel(self.processFrame)
        self.statusLabel.setObjectName(u"statusLabel")
        sizePolicy4 = QSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.statusLabel.sizePolicy().hasHeightForWidth())
        self.statusLabel.setSizePolicy(sizePolicy4)

        self.horizontalLayout_3.addWidget(self.statusLabel)

        self.progressBar = QProgressBar(self.processFrame)
        self.progressBar.setObjectName(u"progressBar")
        sizePolicy5 = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        sizePolicy5.setHorizontalStretch(0)
        sizePolicy5.setVerticalStretch(0)
        sizePolicy5.setHeightForWidth(self.progressBar.sizePolicy().hasHeightForWidth())
        self.progressBar.setSizePolicy(sizePolicy5)
        self.progressBar.setValue(24)

        self.horizontalLayout_3.addWidget(self.progressBar)


        self.verticalLayout_3.addWidget(self.processFrame)

        self.controlOptionStackedWidget = QStackedWidget(self.controlFrame)
        self.controlOptionStackedWidget.setObjectName(u"controlOptionStackedWidget")
        self.controlOptionStackedWidget.setStyleSheet(u"QStackedWidget:{border-bottom:none;}")
        self.controlOptionStackedWidget.setFrameShape(QFrame.StyledPanel)
        self.controlOptionStackedWidget.setFrameShadow(QFrame.Raised)
        self.controlOptionStackedWidget.setLineWidth(3)
        self.controlOptionStackedWidget.setMidLineWidth(3)
        self.rebootOptionPage = QWidget()
        self.rebootOptionPage.setObjectName(u"rebootOptionPage")
        self.formLayout = QFormLayout(self.rebootOptionPage)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setHorizontalSpacing(20)
        self.formLayout.setVerticalSpacing(20)
        self.formLayout.setContentsMargins(20, 20, 20, 20)
        self.label_2 = QLabel(self.rebootOptionPage)
        self.label_2.setObjectName(u"label_2")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label_2)

        self.macLineEdit = QLineEdit(self.rebootOptionPage)
        self.macLineEdit.setObjectName(u"macLineEdit")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.macLineEdit)

        self.label_3 = QLabel(self.rebootOptionPage)
        self.label_3.setObjectName(u"label_3")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_3)

        self.userNameLineEdit = QLineEdit(self.rebootOptionPage)
        self.userNameLineEdit.setObjectName(u"userNameLineEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.userNameLineEdit)

        self.label_4 = QLabel(self.rebootOptionPage)
        self.label_4.setObjectName(u"label_4")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_4)

        self.passwdLineEdit = QLineEdit(self.rebootOptionPage)
        self.passwdLineEdit.setObjectName(u"passwdLineEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.passwdLineEdit)

        self.controlOptionStackedWidget.addWidget(self.rebootOptionPage)
        self.provisionOptionPage = QWidget()
        self.provisionOptionPage.setObjectName(u"provisionOptionPage")
        self.controlOptionStackedWidget.addWidget(self.provisionOptionPage)

        self.verticalLayout_3.addWidget(self.controlOptionStackedWidget)

        self.FixOptionFrame = QFrame(self.controlFrame)
        self.FixOptionFrame.setObjectName(u"FixOptionFrame")
        sizePolicy1.setHeightForWidth(self.FixOptionFrame.sizePolicy().hasHeightForWidth())
        self.FixOptionFrame.setSizePolicy(sizePolicy1)
        self.FixOptionFrame.setMinimumSize(QSize(0, 60))
        self.FixOptionFrame.setStyleSheet(u"QFrame:{border-top:none;}")
        self.FixOptionFrame.setFrameShape(QFrame.StyledPanel)
        self.FixOptionFrame.setFrameShadow(QFrame.Raised)
        self.formLayout_2 = QFormLayout(self.FixOptionFrame)
        self.formLayout_2.setObjectName(u"formLayout_2")
        self.spinBoxLoop = QSpinBox(self.FixOptionFrame)
        self.spinBoxLoop.setObjectName(u"spinBoxLoop")
        self.spinBoxLoop.setMinimum(1)
        self.spinBoxLoop.setMaximum(9999)

        self.formLayout_2.setWidget(0, QFormLayout.FieldRole, self.spinBoxLoop)

        self.labelLoop = QLabel(self.FixOptionFrame)
        self.labelLoop.setObjectName(u"labelLoop")
        self.labelLoop.setMinimumSize(QSize(60, 0))

        self.formLayout_2.setWidget(0, QFormLayout.LabelRole, self.labelLoop)

        self.labelTime = QLabel(self.FixOptionFrame)
        self.labelTime.setObjectName(u"labelTime")

        self.formLayout_2.setWidget(1, QFormLayout.LabelRole, self.labelTime)

        self.spinBoxTime = QSpinBox(self.FixOptionFrame)
        self.spinBoxTime.setObjectName(u"spinBoxTime")
        self.spinBoxTime.setMinimum(1)
        self.spinBoxTime.setMaximum(999)

        self.formLayout_2.setWidget(1, QFormLayout.FieldRole, self.spinBoxTime)


        self.verticalLayout_3.addWidget(self.FixOptionFrame)


        self.horizontalLayout.addWidget(self.controlFrame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 800, 23))
        self.menuMenu = QMenu(self.menubar)
        self.menuMenu.setObjectName(u"menuMenu")
        self.menuOther = QMenu(self.menubar)
        self.menuOther.setObjectName(u"menuOther")
        self.menuUI = QMenu(self.menuOther)
        self.menuUI.setObjectName(u"menuUI")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuMenu.menuAction())
        self.menubar.addAction(self.menuOther.menuAction())
        self.menuOther.addAction(self.actionAboutShow)
        self.menuOther.addSeparator()
        self.menuOther.addAction(self.menuUI.menuAction())
        self.menuUI.addAction(self.actionLight_Blue)
        self.menuUI.addAction(self.actionDark_Blue)
        self.menuUI.addAction(self.actionLight_Cyan)
        self.menuUI.addAction(self.actionLight_Pink)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionAbout.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionAboutShow.setText(QCoreApplication.translate("MainWindow", u"About", None))
        self.actionUI_Light_Blue.setText(QCoreApplication.translate("MainWindow", u"UI: Light-Blue", None))
        self.actionDark_Blue.setText(QCoreApplication.translate("MainWindow", u"Dark-Blue", None))
        self.actionLight_Blue.setText(QCoreApplication.translate("MainWindow", u"Light-Blue", None))
        self.actionLight_Cyan.setText(QCoreApplication.translate("MainWindow", u"Light-Cyan", None))
        self.actionLight_Pink.setText(QCoreApplication.translate("MainWindow", u"Light-Pink", None))
        self.pushButtonStart.setText(QCoreApplication.translate("MainWindow", u"Start", None))
        self.pushButtonStop.setText(QCoreApplication.translate("MainWindow", u"Stop", None))
        self.textBrowser.setHtml(QCoreApplication.translate("MainWindow", u"<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:'SimSun'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">Welcome</p></body></html>", None))
        self.statusLabel.setText(QCoreApplication.translate("MainWindow", u"Running", None))
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Mac:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"User Name:", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Password:", None))
        self.labelLoop.setText(QCoreApplication.translate("MainWindow", u"Loop:", None))
        self.labelTime.setText(QCoreApplication.translate("MainWindow", u"Time:", None))
        self.menuMenu.setTitle(QCoreApplication.translate("MainWindow", u"Menu", None))
        self.menuOther.setTitle(QCoreApplication.translate("MainWindow", u"Other", None))
        self.menuUI.setTitle(QCoreApplication.translate("MainWindow", u"UI Change", None))
    # retranslateUi

