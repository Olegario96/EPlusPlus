import sys
from PyQt5.QtWidgets import QApplication
from eplusplus.view import MainWindow

app = QApplication(list(sys.argv))
mainWindow = MainWindow()
sys.exit(app.exec_())