import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QFileDialog, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap, QIcon

class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.firstTime = True

        self.logo = QLabel()
        self.casesButton = QPushButton("Gerar casos")
        self.simulationButton = QPushButton("Executar simulação") 
        self.confirmButton = QPushButton("Confirmar")
        self.cancelButton = QPushButton("Cancelar")
        self.lineIdf = QLineEdit()
        self.vLayout = QVBoxLayout()
        self.initComponents()

    def initComponents(self):
        self.casesButton.clicked.connect(self.casesButtonClicked)
        self.cancelButton.clicked.connect(self.cancelButtonClicked)

        pixmap = QPixmap("logo.png")
        self.logo.setPixmap(pixmap)

        self.vLayout.addWidget(self.logo)
        self.vLayout.addWidget(self.casesButton)
        self.vLayout.addWidget(self.simulationButton)

        if self.firstTime:
            self.firstTime = False
            self.setLayout(self.vLayout)
            self.setFixedSize(300, 200)
            self.setWindowTitle("EPlusPlus")
            self.show()

    def casesButtonClicked(self):
        for component in reversed(range(self.vLayout.count())):
            self.vLayout.itemAt(component).widget().setParent(None)

        idfLabel = QLabel()
        csvLabel = QLabel()
        folderStoreLabel = QLabel()

        idfLabel.setText("Arquivo base idf:")
        csvLabel.setText("Arquivo de configuração CSV:")
        folderStoreLabel.setText("Pasta para salvar os arquivos CSV's:")

        self.lineIdf.returnPressed.connect(self.lineIdfClicked)

        self.vLayout.addWidget(idfLabel)
        self.vLayout.addWidget(self.lineIdf)
        self.vLayout.addWidget(csvLabel)
        self.vLayout.addWidget(folderStoreLabel)
        self.vLayout.addWidget(self.confirmButton)
        self.vLayout.addWidget(self.cancelButton)

    def lineIdfClicked(self):
        print(1)

    def cancelButtonClicked(self):
        for component in reversed(range(self.vLayout.count())):
            self.vLayout.itemAt(component).widget().setParent(None)

        self.initComponents()

    def mousePressEventIdf(self, event):
        super(self.lineIdf, self).mousePressedEvent(event)
        if event.button() == "QtCore.Qt.LeftButton":
            pass

app = QApplication(sys.argv)
mainWindow = MainWindow()
sys.exit(app.exec_())
