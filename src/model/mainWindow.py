import os
import ctypes
from .lineEditDialog import LineEditDialog
from eplusplus.controller import ActorUser
from eplusplus.model import PlatformManager
from eplusplus.exception import ColumnException
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QRadioButton
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QMessageBox
from PyQt5.QtWidgets import QButtonGroup, QLineEdit

##
## @brief      This class implements the main window of the eplusplus
##             application. The UI use the PyQt to create and configure
##             all the components. Also, besides the components like
##             labels, radio buttons, buttons and line text, the main
##             window has a actorUser, that represents the controller, to call
##             all the functions implemented in the logic of the program.
##
class MainWindow(QWidget):
    def __init__(self):
        super(MainWindow, self).__init__()

        self.firstTime = True
        self.pathToIcon = "../media/img/icon.png"
        self.platformManager = PlatformManager()
        self.actorUser = ActorUser()

        self.logo = QLabel()

        self.casesButton = QPushButton("Gerar casos")
        self.simulationButton = QPushButton("Executar simulação")
        self.confirmButton = QPushButton("Confirmar")
        self.cancelButton = QPushButton("Cancelar")
        self.chooseIdfButton = QPushButton("Escolher arquivo...")
        self.chooseCSVButton = QPushButton("Escolher arquivo...")
        self.chooseFolderButton = QPushButton("Escolher pasta...")

        self.setWindowIcon(QIcon(self.pathToIcon))

        self.lineIdf = LineEditDialog(self)
        self.lineCsv = LineEditDialog(self)
        self.lineFolder = LineEditDialog(self)
        self.lineCases = QLineEdit()
        self.validatorCases = QIntValidator(0, 9999999, self)
        self.lineCases.setValidator(self.validatorCases)

        self.group = QButtonGroup()
        self.lhsRB = QRadioButton("Latin Hypercube Sampling")
        self.randomRB = QRadioButton("Random")
        self.group.addButton(self.randomRB)
        self.group.addButton(self.lhsRB)

        self.gridLayout = QGridLayout()
        self.initComponents()


    ##
    ## @brief      This method is called at the constructor method or
    ##             a cancel button is clicked to go back to the first screen.
    ##             This method configures the layout. Also if is the first
    ##             time that this method is called, then all buttons will
    ##             be connected to the corresponding method.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def initComponents(self):
        pixmap = QPixmap("../media/img/title.png")
        self.logo.setPixmap(pixmap)

        if (self.platformManager.isWindows()):
            appid = 'LabEEE.EPlusPlus.V0.8'
            ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(appid)

        self.gridLayout.addWidget(self.logo, 0, 0)
        self.gridLayout.addWidget(self.casesButton, 1, 0)
        self.gridLayout.addWidget(self.simulationButton, 2, 0)

        if self.firstTime:
            self.firstTime = False

            self.casesButton.clicked.connect(self.casesButtonClicked)
            self.cancelButton.clicked.connect(self.cancelButtonClicked)
            self.confirmButton.clicked.connect(self.confirmButtonClicked)
            self.chooseIdfButton.clicked.connect(self.chooseIdfClicked)
            self.chooseCSVButton.clicked.connect(self.chooseCsvClicked)
            self.chooseFolderButton.clicked.connect(self.chooseFolderClicked)

            self.setLayout(self.gridLayout)
            self.setFixedSize(470, 230)
            self.setWindowTitle("EPlusPlus")
            self.show()

    ##
    ## @brief      This method is actived whenever the "casesButton" is
    ##             pressed. First of all, it remove all components from
    ##             the window. After that it justs configures labels,
    ##             lineTexts and buttons into the grid layout.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def casesButtonClicked(self):
        self.clearAll()

        idfLabel = QLabel()
        csvLabel = QLabel()
        folderStoreLabel = QLabel()
        methodSamplingLabel = QLabel()
        sampleSize = QLabel()

        idfLabel.setText("Arquivo base idf:")
        csvLabel.setText("Arquivo de configuração CSV:")
        folderStoreLabel.setText("Pasta para salvar os arquivos CSV's:")
        methodSamplingLabel.setText("Método de amostragem")
        sampleSize.setText("Número da amostragem")

        self.gridLayout.addWidget(idfLabel, 1, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.chooseIdfButton, 1, 1)
        self.gridLayout.addWidget(self.lineIdf, 1, 2)

        self.gridLayout.addWidget(csvLabel, 2, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.chooseCSVButton, 2, 1)
        self.gridLayout.addWidget(self.lineCsv, 2, 2)

        self.gridLayout.addWidget(folderStoreLabel, 3, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.chooseFolderButton, 3, 1)
        self.gridLayout.addWidget(self.lineFolder, 3, 2)

        self.gridLayout.addWidget(methodSamplingLabel, 4, 1, Qt.AlignBottom)
        self.gridLayout.addWidget(self.randomRB, 5, 0, Qt.AlignTop)
        self.gridLayout.addWidget(self.lhsRB, 5, 2, Qt.AlignTop)

        self.gridLayout.addWidget(sampleSize, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.lineCases, 6, 2, 1, 3, Qt.AlignCenter)

        self.gridLayout.addWidget(self.confirmButton, 7, 0, 1, 3, Qt.AlignTop)
        self.gridLayout.addWidget(self.cancelButton, 8, 0, 1, 3, Qt.AlignTop)


    ##
    ## @brief      This method is actived whenever the "chooseIdf" button is
    ##             pressed. When this method is activated, a QFileDialog will
    ##             be show to the user and it will be possible to choose a
    ##             idf file. The QFileDialog will show only idf files and
    ##             folders. After choosed the idf file, the "lineIdf" attribute
    ##             will have its text setted to the absolute path to the csv
    ##             choosed.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def chooseIdfClicked(self):
        msg = "Escolha o arquivo idf"
        filename = QFileDialog.getOpenFileName(self, msg, os.getenv("HOME"), filter="*.idf")
        self.setLineIdfText(filename[0])

    ##
    ## @brief      This method is actived whenever the "chooseCsv" buttons is
    ##             pressed. When this method is activated, a QFileDialog will
    ##             be show to the user and it will be possible to choose a
    ##             csv file. After choosed the csv file, the "lineCsv"
    ##             attribute will have its text setted to the absolute path
    ##             to the csv choosed.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def chooseCsvClicked(self):
        msg = "Escolha o arquivo base csv"
        filename = QFileDialog.getOpenFileName(self, msg, os.getenv("HOME"), filter="*.csv")
        self.setLineCsvText(filename[0])

    ##
    ## @brief      This method is actived whenever the "chooseFolder" button is
    ##             clicked. When this method is activated, a QFileDialog will
    ##             be show to the user and it will be possible to choose a
    ##             folder to save the new idf's files that gonna be generated.
    ##             After choosed the folder, the "lineFolder" attribute
    ##             will have its text changed to the absolute folder choosed.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def chooseFolderClicked(self):
        msg = "Escolha a pasta para salvar os arquivos IDF's"
        folder = QFileDialog.getExistingDirectory(self, msg, os.getenv("HOME"))
        self.setLineFolderText(folder)

    ##
    ## @brief      This method is activated when the cancel button is
    ##             pressed. This method remove all components from the
    ##             screen and go back to the initial screen.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def cancelButtonClicked(self):
        self.clearAll()
        self.initComponents()

    ##
    ## @brief      This method is actived whenever the confirm button
    ##             is pressed. This method checks if all the lineText
    ##             fields where filled and one radio button. If not, the
    ##             user will be informed through a QMessageBox. Otherwise,
    ##             if all fields where covered then the cases will be generate.
    ##             See the "generateCases" method for more info.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def confirmButtonClicked(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QIcon(self.pathToIcon))
        msgBox.setWindowTitle("EPlusPlus-WAR")
        msgBox.setText("Todos os campos devem estar preenchidos para prosseguir!")

        if self.lineIdf.text() == "":
            msgBox.exec_()
        elif self.lineCsv.text() == "":
            msgBox.exec_()
        elif self.lineFolder.text() == "":
            msgBox.exec_()
        elif self.lineCases.text() == "":
            msgBox.exec_()
        elif not self.lhsRB.isChecked() and not self.randomRB.isChecked():
            msgBox.exec_()
        else:
            self.generateCases()

    ##
    ## @brief      This method takes all values informed by the user through
    ##             the lineEdit fields. After analyze the sampling method
    ##             choosed, the UI will call the actorUser to generate
    ##             the cases. If all happens as it should, then a QmessageBox
    ##             will inform the user. Otherwise, if a "ColumnException"
    ##             raise from the the "actorUser", the user will be informed
    ##             that the Csv or the Idf are not matching.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def generateCases(self):
        pathToIdf = self.lineIdf.text()
        pathToCsv = self.lineCsv.text()
        pathToFolder = self.lineFolder.text()
        sampleSize = int(self.lineCases.text())
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(self.pathToIcon))
        msg = ""

        if self.lhsRB.isChecked():
            method = "LHS"
        else:
            method = "RANDOM"

        try:
            self.actorUser.generateCases(pathToIdf, pathToCsv, pathToFolder, sampleSize, method)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("EPlusPlus-INF")
            msg = "Processo finalizado! Verifique a pasta informada para acessar os arquivos."
            msgBox.setText(msg)
            msgBox.exec_()
        except ColumnException as e:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("EPlusPlus-ERR")
            msg = "O arquivo csv ou o arquivo idf não estão no formato correto!"
            msgBox.setText(msg)
            msgBox.exec_()

    ##
    ## @brief      This method removes every component at the current window,
    ##             except for the layout. Also, this method clear all lineText
    ##             attributes and clear the values of the radio buttons. The
    ##             "setExclusive" False and "setExclusive" True is needed to
    ##             clear the values of the radio button components.
    ##
    ## @param      self  Non static method.
    ##
    ## @return     This is a void method.
    ##
    def clearAll(self):
        for component in reversed(range(self.gridLayout.count())):
            self.gridLayout.itemAt(component).widget().setParent(None)

        self.setLineIdfText("")
        self.setLineCsvText("")
        self.setLineFolderText("")
        self.setLineCasesText("")
        self.group.setExclusive(False)
        self.randomRB.setChecked(False)
        self.lhsRB.setChecked(False)
        self.group.setExclusive(True)


    ##
    ## @brief      This method sets the first lineText of the 2nd screen
    ##             with the string equals to the path where the idf file
    ##             is saved, informed by the user through the QFileDialog.
    ##
    ## @param      self    The object
    ## @param      string  String that will be show at the lineText.
    ##
    ## @return     This is a void method.
    ##
    def setLineIdfText(self, string):
        self.lineIdf.setText(string)

    ##
    ## @brief      This method sets the second lineText of the 2nd
    ##             screen with the string equals to the path where
    ##             the csv file is saved, choosed by the user.
    ##
    ## @param      self    Non static method.
    ## @param      string  String that will be show at the lineText.
    ##
    ## @return     This is a void method.
    ##
    def setLineCsvText(self, string):
        self.lineCsv.setText(string)

    ##
    ## @brief      This method sets the third lineText of the 2nd
    ##             screen with the string equals to the path where the new
    ##             idf's file will be saved, choosed by the user.
    ##
    ## @param      self    Non static method.
    ## @param      string  String that will be show at the lineText.
    ##
    ## @return     This is a void method.
    ##
    def setLineFolderText(self, string):
        self.lineFolder.setText(string)

    ##
    ## @brief      This method sets the fourth lineText of the 2nd screen
    ##             with the value equals to the string passed as arg.
    ##
    ## @param      self    The object
    ## @param      string  String that will be show at the lineCases
    ##
    ## @return     This is a void method
    ##
    def setLineCasesText(self, string):
        self.lineCases.setText(string)