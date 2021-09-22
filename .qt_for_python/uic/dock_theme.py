# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'dock_theme.ui'
##
## Created by: Qt User Interface Compiler version 6.1.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import *  # type: ignore
from PySide6.QtGui import *  # type: ignore
from PySide6.QtWidgets import *  # type: ignore


class Ui_DockWidget(object):
    def setupUi(self, DockWidget):
        if not DockWidget.objectName():
            DockWidget.setObjectName(u"DockWidget")
        DockWidget.resize(231, 391)
        self.dockWidgetContents = QWidget()
        self.dockWidgetContents.setObjectName(u"dockWidgetContents")
        self.gridLayout = QGridLayout(self.dockWidgetContents)
        self.gridLayout.setObjectName(u"gridLayout")
        self.formLayout = QFormLayout()
        self.formLayout.setObjectName(u"formLayout")
        self.pushButton_primaryColor = QPushButton(self.dockWidgetContents)
        self.pushButton_primaryColor.setObjectName(u"pushButton_primaryColor")

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.pushButton_primaryColor)

        self.pushButton_primaryLightColor = QPushButton(self.dockWidgetContents)
        self.pushButton_primaryLightColor.setObjectName(u"pushButton_primaryLightColor")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.pushButton_primaryLightColor)

        self.pushButton_secondaryColor = QPushButton(self.dockWidgetContents)
        self.pushButton_secondaryColor.setObjectName(u"pushButton_secondaryColor")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.pushButton_secondaryColor)

        self.pushButton_secondaryLightColor = QPushButton(self.dockWidgetContents)
        self.pushButton_secondaryLightColor.setObjectName(u"pushButton_secondaryLightColor")

        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.pushButton_secondaryLightColor)

        self.pushButton_secondaryDarkColor = QPushButton(self.dockWidgetContents)
        self.pushButton_secondaryDarkColor.setObjectName(u"pushButton_secondaryDarkColor")

        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.pushButton_secondaryDarkColor)

        self.pushButton_primaryTextColor = QPushButton(self.dockWidgetContents)
        self.pushButton_primaryTextColor.setObjectName(u"pushButton_primaryTextColor")

        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.pushButton_primaryTextColor)

        self.pushButton_secondaryTextColor = QPushButton(self.dockWidgetContents)
        self.pushButton_secondaryTextColor.setObjectName(u"pushButton_secondaryTextColor")

        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.pushButton_secondaryTextColor)

        self.checkBox_ligh_theme = QCheckBox(self.dockWidgetContents)
        self.checkBox_ligh_theme.setObjectName(u"checkBox_ligh_theme")

        self.formLayout.setWidget(7, QFormLayout.FieldRole, self.checkBox_ligh_theme)


        self.gridLayout.addLayout(self.formLayout, 0, 0, 1, 1)

        DockWidget.setWidget(self.dockWidgetContents)

        self.retranslateUi(DockWidget)

        QMetaObject.connectSlotsByName(DockWidget)
    # setupUi

    def retranslateUi(self, DockWidget):
        DockWidget.setWindowTitle(QCoreApplication.translate("DockWidget", u"Change Theme", None))
        self.pushButton_primaryColor.setText(QCoreApplication.translate("DockWidget", u"primaryColor", None))
        self.pushButton_primaryLightColor.setText(QCoreApplication.translate("DockWidget", u"primaryLightColor", None))
        self.pushButton_secondaryColor.setText(QCoreApplication.translate("DockWidget", u"secondaryColor", None))
        self.pushButton_secondaryLightColor.setText(QCoreApplication.translate("DockWidget", u"secondaryLightColor", None))
        self.pushButton_secondaryDarkColor.setText(QCoreApplication.translate("DockWidget", u"secondaryDarkColor", None))
        self.pushButton_primaryTextColor.setText(QCoreApplication.translate("DockWidget", u"primaryTextColor", None))
        self.pushButton_secondaryTextColor.setText(QCoreApplication.translate("DockWidget", u"secondaryTextColor", None))
        self.checkBox_ligh_theme.setText(QCoreApplication.translate("DockWidget", u"Invert secondary colors", None))
    # retranslateUi

