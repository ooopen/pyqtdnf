from pstats import Stats

from PyQt5 import uic
from PyQt5.QtWidgets import QMessageBox, QApplication, QPushButton, QLineEdit, QWidget, QMainWindow

from ui.main import Ui_MainWindow


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.handleCalc)

    def handleCalc(self):
        t = self.ui.lineEdit.text()
        print(t)


app = QApplication([])
stats = MainWindow()
stats.show()
app.exec_()
