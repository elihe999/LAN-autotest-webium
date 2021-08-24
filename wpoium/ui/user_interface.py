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
from PySide6.QtCore import QEnum, QFlag, QObject, Qt, Signal, Slot, QThread, \
    QFile, QIODevice, QTextStream, QByteArray
# WARNING:root:qt_material must be imported after PySide or PyQt!
from qt_material import QtStyleTools
import os
import json

from wpoium.ui.worker import BackgroundWorker


class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    sendsignal = Signal(str, str, str, int, int)

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
        self.background_worker_.finished.connect(self.stopTest)

        ################################################################
        self.style_name = "light_blue.xml"
        # self.apply_stylesheet(self.main, 'light_blue.xml')
        self.main.actionDark_Blue.triggered.connect(
            lambda: self.changeStyle('dark_teal.xml'))
        self.main.actionLight_Blue.triggered.connect(
            lambda: self.changeStyle('light_blue.xml'))
        self.main.actionLight_Cyan.triggered.connect(
            lambda: self.changeStyle('light_cyan.xml'))
        self.main.actionLight_Pink.triggered.connect(
            lambda: self.changeStyle('light_pink.xml'))
        self.main.actionDark_Amber.triggered.connect(
            lambda: self.changeStyle('dark_amber.xml'))
        self.main.actionDark_Cyan.triggered.connect(
            lambda: self.changeStyle('dark_cyan.xml'))
        self.main.actionDark_LightGreen.triggered.connect(
            lambda: self.changeStyle('dark_lightgreen.xml'))
        self.main.actionDark_Purple.triggered.connect(
            lambda: self.changeStyle('dark_purple.xml'))
        self.main.actionDark_Yellow.triggered.connect(
            lambda: self.changeStyle('dark_yellow.xml'))

        self.style_list = ['dark_amber.xml',
                            'dark_blue.xml',
                            'dark_cyan.xml',
                            'dark_lightgreen.xml',
                            'dark_pink.xml',
                            'dark_purple.xml',
                            'dark_red.xml',
                            'dark_teal.xml',
                            'dark_yellow.xml',
                            'light_amber.xml',
                            'light_blue.xml',
                            'light_cyan.xml',
                            'light_cyan_500.xml',
                            'light_lightgreen.xml',
                            'light_pink.xml',
                            'light_purple.xml',
                            'light_red.xml',
                            'light_teal.xml',
                            'light_yellow.xml']
        # ============================================
        # variable
        # ============================================
        self.suite_name = ""
        self.config = None
        self.wait_time = 0
        self.total_loop = 0
        # ============================================
        # option var cache
        # ============================================
        file = QFile("cache")
        if not file.open(QIODevice.ReadOnly | QIODevice.Text):
            return
        inStream = QTextStream(file)
        self.main.macLineEdit.setText(inStream.readLine())
        self.main.userNameLineEdit.setText(inStream.readLine())
        self.main.passwdLineEdit.setText(inStream.readLine())
        _spinV = inStream.readLine()
        if _spinV == "" or int(_spinV) < 0:
            self.main.spinBoxLoop.setValue(0)
        else:
            self.main.spinBoxLoop.setValue(int(_spinV))
        _spinT = inStream.readLine()
        if _spinT == "" or int(_spinT) < 0:
            self.main.spinBoxTime.setValue(0)
        else:
            self.main.spinBoxTime.setValue(int(_spinT))
        #
        style_name = str(inStream.readLine())
        if style_name in self.style_list:
            self.style_name = style_name
        self.changeStyle(self.style_name)
        file.close()

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

    def changeStyle(self, name):
        self.apply_stylesheet(self.main, name)
        self.style_name = name
        self.saveCache()

    def saveCache(self):
        file = QFile("cache")
        if not file.open(QIODevice.WriteOnly):
            return
        content = self.main.macLineEdit.text() + "\n"
        content += self.main.userNameLineEdit.text() + "\n"
        content += self.main.passwdLineEdit.text() + "\n"
        content += str(self.main.spinBoxLoop.value()) + "\n"
        content += str(self.main.spinBoxTime.value()) + "\n"
        content += self.style_name + "\n"
        # write
        byteArr = bytes(content, "utf-8")
        file.write(QByteArray(byteArr))
        file.close()

    def checkParamVaild(self):
        if self.suite_name != "":
            now_day = time.strftime("%Y_%m_%d")
            now_time = time.strftime("%H_%M_%S")
            if not os.path.exists( os.path.join(self.config.report_dir, now_day) ):
                os.mkdir(os.path.join(self.config.report_dir, now_day))
            folder_name = os.path.join(self.config.report_dir, now_day)
            os.mkdir(os.path.join(folder_name, now_time))
            os.mkdir(os.path.join(folder_name, now_time) + "/image")
            self.config.NEW_REPORT = os.path.join(folder_name, now_time)
            self.config.html_report = os.path.join(self.config.NEW_REPORT, "report.html")
            #
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
            self.wait_time = int(sleep_time)
            self.total_loop = int(loop_num)
            # {"name": "admin", "passwd": "123", "mac": "c0:74:ad:28:b2:1a"}
            self.saveCache()
            self.sendsignal.emit(
                os.path.join(self.config.cases_path, self.suite_name),
                self.config.html_report,
                base_meta,
                int(sleep_time),
                int(loop_num))
           
    def changeSeletedCase(self, case_name):
        self.suite_name = "test_"+case_name+".py"


    ######          SOLT            ######
    @Slot()
    def stopTest(self, loop):
        """"""
        if not self.background_worker_thread_.isRunning():
            self.background_worker_thread_.quit()
        self.main.statusLabel.setText("Stopped")
        vp = (loop+1/self.total_loop) * 100
        vp = 100 if vp > 100 else vp
        self.main.progressBar.setValue(vp)

    @Slot()
    def showResult(self, loop, timeing, status):
        self.main.pushButtonStart.setEnabled(False)
        index_name = str(loop+1)
        if status == 1:
            self.main.statusLabel.setText(
                "Waiting.."+str(self.wait_time - timeing))
            vp = (loop+1/self.total_loop) * 100
            self.main.progressBar.setValue(vp)
        if status == 0:
            self.main.statusLabel.setText(
                "Running: "+index_name+"/"+str(self.total_loop))
    
    @Slot()
    def updateLogs(self, append_log):
        self.main.logBrowser.append(str(append_log) + "\n")


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
