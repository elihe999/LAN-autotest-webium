# -*- coding: utf-8 -*-

from PySide6.QtCore import QObject, Signal, qDebug, QThread, Slot
import time
import pytest


class BackgroundWorker(QObject):
    report_progress = Signal(int, int, int)
    finished = Signal(int)
    report = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.is_cancelled_ = False
        self.progress_ = 0
        self.current_loop = 0
        self.total_loop = 0

    @Slot()
    def run(self, name, html, meta, delay, loop):
        self.total_loop = loop
        while self.current_loop < self.total_loop:
            print("#\tTest: \t " + str(self.current_loop + 1) +
                  "/" + str(self.total_loop) + "\t.")
            self.report_progress.emit(self.current_loop, 1, 0)
            pytest.main(["-v", "-s", name,
                         '--metadata-from-json='+meta, '--repeat-scope=session', "--self-contained-html", "--html=" + html])
            self.ticker(delay)
            self.current_loop = self.current_loop + 1
        self.finished.emit(self.current_loop)

    def cancel(self):
        self.is_cancelled_ = True
        qDebug('cancelled...thread id: '+str(QThread.currentThread()))

    def reset(self):
        self.is_cancelled_ = False
        self.progress_ = 0

    def ticker(self, count):
        for i in range(count):
            time.sleep(1)
            if self.is_cancelled_ == True:
                self.quit()
                break
            self.report_progress.emit(self.current_loop, i, 1)

    def quit(self):
        print("Quit Func: ")
