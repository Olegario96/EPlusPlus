import os
import sys
from lineEditDialog import LineEditDialog
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QMessageBox
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
        self.chooseIdfButton = QPushButton("Escolher arquivo...")
        self.chooseCSVButton = QPushButton("Escolher arquivo...")
        self.chooseFolderButton = QPushButton("Escolher pasta...")

        self.lineIdf = LineEditDialog(self)
        self.lineCsv = LineEditDialog(self)
        self.lineFolder = LineEditDialog(self)

        self.gridLayout = QGridLayout()
        self.initComponents()

    def initComponents(self):
        pixmap = QPixmap("logo.png")
        self.logo.setPixmap(pixmap)

        self.gridLayout.addWidget(self.logo, 0, 0)
        self.gridLayout.addWidget(self.casesButton, 1, 0)
        self.gridLayout.addWidget(self.simulationButton, 2, 0)

        if self.firstTime:
            self.casesButton.clicked.connect(self.casesButtonClicked)
            self.cancelButton.clicked.connect(self.cancelButtonClicked)
            self.confirmButton.clicked.connect(self.confirmButtonClicked)
            self.chooseIdfButton.clicked.connect(self.chooseIdfClicked)
            self.chooseCSVButton.clicked.connect(self.chooseCsvClicked)
            self.chooseFolderButton.clicked.connect(self.chooseFolderClicked)

            self.firstTime = False
            self.setLayout(self.gridLayout)
            self.setFixedSize(470, 300)
            self.setWindowTitle("EPlusPlus")
            self.show()

    def casesButtonClicked(self):
        self.removeAll()

        idfLabel = QLabel()
        csvLabel = QLabel()
        folderStoreLabel = QLabel()

        idfLabel.setText("Arquivo base idf:")
        csvLabel.setText("Arquivo de configuração CSV:")
        folderStoreLabel.setText("Pasta para salvar os arquivos CSV's:")

        self.gridLayout.addWidget(idfLabel, 1, 0, 1, 2)
        self.gridLayout.addWidget(self.chooseIdfButton, 1, 1)
        self.gridLayout.addWidget(self.lineIdf, 1, 2)

        self.gridLayout.addWidget(csvLabel, 2, 0)
        self.gridLayout.addWidget(self.chooseCSVButton, 2, 1)
        self.gridLayout.addWidget(self.lineCsv, 2, 2)

        self.gridLayout.addWidget(folderStoreLabel, 3, 0)
        self.gridLayout.addWidget(self.chooseFolderButton, 3, 1)
        self.gridLayout.addWidget(self.lineFolder, 3, 2)

        self.gridLayout.addWidget(self.confirmButton, 4, 0, 1, 3)
        self.gridLayout.addWidget(self.cancelButton, 5, 0, 1, 3)

    def chooseIdfClicked(self):
        msg = "Escolha o arquivo idf"
        filename = QFileDialog.getOpenFileName(self, msg, os.getenv("HOME"), filter="*.idf")
        self.setLineIdfText(filename[0])    

    def chooseCsvClicked(self):
        msg = "Escolha o arquivo base csv"
        filename = QFileDialog.getOpenFileName(self, msg, os.getenv("HOME"), filter="*.csv")
        self.setLineCsvText(filename[0])

    def chooseFolderClicked(self):
        msg = "Escolha a pasta para salvar os arquivos IDF's"
        folder = QFileDialog.getExistingDirectory(self, msg, os.getenv("HOME"))
        self.setLineFolderText(folder)

    def cancelButtonClicked(self):
        self.removeAll()
        self.setLineIdfText("")
        self.setLineCsvText("")
        self.setLineFolderText("")
        self.initComponents()

    def confirmButtonClicked(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowTitle("EPlusPlus-WARNING")
        msgBox.setText("Todos os campos devem estar preenchidos para prosseguir!")

        if self.lineIdf.text() == "":
            msgBox.exec_()
        elif self.lineCsv.text() == "":
            msgBox.exec_()
        elif self.lineFolder.text() == "":
            msgBox.exec_()
        else:
            print("dale")

    def removeAll(self):
        for component in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(component).widget().setParent(None)

    def setLineIdfText(self, string):
        self.lineIdf.setText(string)

    def setLineCsvText(self, string):
        self.lineCsv.setText(string)

    def setLineFolderText(self, string):
        self.lineFolder.setText(string)

app = QApplication(list(sys.argv))
mainWindow = MainWindow()
sys.exit(app.exec_())
