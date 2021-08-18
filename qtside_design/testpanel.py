from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtUiTools import QUiLoader
from PySide6.QtGui import QFontDatabase
from qt_material import QtStyleTools

class RuntimeStylesheets(QMainWindow, QtStyleTools):
    # ----------------------------------------------------------------------
    def __init__(self):
        """"""
        super().__init__()
        self.main = QUiLoader().load('autotest_wig.ui', self)
        self.apply_stylesheet(self.main, 'light_blue.xml')
        self.main.actionDark_Blue.triggered.connect(lambda: self.apply_stylesheet(self.main, 'dark_teal.xml'))
        self.main.actionLight_Blue.triggered.connect(lambda: self.apply_stylesheet(self.main, 'light_blue.xml'))


if __name__ == "__main__":
    app = QApplication()

    # Local file
    QFontDatabase.addApplicationFont('JiZiJingDianFangSongJianFan-Shan-2.ttf')

    frame = RuntimeStylesheets()
    frame.main.show()

    app.exec_()