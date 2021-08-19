
import example_gui
from PySide6.QtCore import *
from PySide6.QtGui import *
from PySide6.QtWidgets import *
from PySide6.QtUiTools import QUiLoader

import PySide6
import sys
import time

class Pencere(QMainWindow,example_gui.Ui_MainWindow):
    def __init__(self,parent=None):
        super(Pencere,self).__init__(parent)
        self.setupUi(self)

        
        self.task1 = scroller(self.work_progressBar,0.1)
        self.task2 = scroller(self.eat_progressBar,0.2)
        self.task3 = scroller(self.sleep_progressBar,0.5)
        
        self.workButton.clicked.connect(self.workButtonGO)
        self.eatButton.clicked.connect(self.eatButtonGO)
        self.sleepButton.clicked.connect(self.sleepButtonGO)
        
    def workButtonGO(self):
        self.task1.start()
        self.task1.updatesignal.connect(self.work_progressBar.setValue)
        
    def eatButtonGO(self):
        self.task2.start()
        self.task2.updatesignal.connect(self.eat_progressBar.setValue)
        
    def sleepButtonGO(self):
        self.task3.start()
        self.task3.updatesignal.connect(self.sleep_progressBar.setValue)
    
    
class scroller(QThread):
    updatesignal=Signal(int)
    
    def __init__(self,delta_t = float, parent=None):
        super(scroller, self).__init__(parent)
        self.obj=obj
        self.delta=delta_t
    def run(self):
        for c in range(100):
            self.updatesignal.emit(c)
            time.sleep(self.delta)        
    
    def terminated(self):
        self.wait()
    


app=QApplication(sys.argv)
form=Pencere()
form.show()
app.exec_()