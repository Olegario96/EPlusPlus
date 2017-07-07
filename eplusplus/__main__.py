import sys
from PyQt5.QtWidgets import QApplication
from eplusplus.view import MainWindow

args = list(sys.argv)
app = QApplication(args)
mainWindow = MainWindow(args)
sys.exit(app.exec_())
