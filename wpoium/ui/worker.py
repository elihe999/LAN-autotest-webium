# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal, qDebug, QThread, Slot
import time
class BackgroundWorker(QObject):
    report_progress = Signal(int)
    finished = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_cancelled_ = False
        self.progress_ = 0

    @Slot()
    def run(self, name, loop):
        while(1):
            time.sleep(1)
            print(1)
            self.report_progress.emit("1")

    def cancel(self):
        self.is_cancelled_ = True
        qDebug('cancelled...thread id: '+str(QThread.currentThread()))

    def reset(self):
        self.is_cancelled_ = False
        self.progress_ = 0