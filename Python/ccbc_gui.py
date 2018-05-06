#!/usr/bin/env Python3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication
from theGUI import Ui_MainWindow
from ccbc_control import CCBC_Brains

class ccbcGUI(QMainWindow, Ui_MainWindow):

    def __init__(self, ccbc):
        super(self.__class__, self).__init__()
        self.setupUi(self)
        self.ccbc = ccbc
        self.show()

    def start_serial(self):


if __name__ == "__main__":
    ccbc = CCBC_Brains()
    app = QApplication(sys.argv)
    ccbc = ccbcGUI()
    app.exec()

