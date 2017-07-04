import os
import ctypes
import webbrowser
from .lineEdit import LineEdit
from eplusplus.controller import ActorUser
from eplusplus.exception import ColumnException, NoIdfException
from PyQt5.QtCore import QSize, Qt, QRect
from PyQt5.QtGui import QPixmap, QIcon, QIntValidator
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QRadioButton
from PyQt5.QtWidgets import QGridLayout, QFileDialog, QMessageBox, QApplication
from PyQt5.QtWidgets import QButtonGroup, QLineEdit, QAction, QMenuBar

##
## @brief      This class implements the main window of the eplusplus
##             application. The UI use the PyQt to create and configure
##             all the components. Also, besides the components like
##             labels, radio buttons, buttons and line text, the main
##             window has a actorUser, that represents the controller, to call
##             all the methods implemented in the logic of the program.
##
class MainWindow(QWidget):
    def __init__(self, args):
        super(MainWindow, self).__init__()
        self.args = args

        self.firstTime = True

        if len(self.args) > 1:
            self.pathToIcon = "../media/img/icon.png"
        else:
            self.pathToIcon = "./Images/icon.png"

        self.actorUser = ActorUser()

        self.logo = QLabel()

        self.casesButton = QPushButton("Gerar casos")
        self.simulationButton = QPushButton("Executar simulação")
        self.confirmButtonCases = QPushButton("Confirmar")
        self.cancelButton = QPushButton("Cancelar")
        self.chooseIdfButton = QPushButton("Escolher IDF...")
        self.chooseCSVButton = QPushButton("Escolher CSV...")
        self.chooseFolderButton = QPushButton("Escolher pasta...")
        self.chooseEpwButton = QPushButton("Escolher EPW...")
        self.confirmButtonSimulation = QPushButton("Confirmar")

        self.setWindowIcon(QIcon(self.pathToIcon))

        self.lineIdf = LineEdit(self)
        self.lineCsv = LineEdit(self)
        self.lineFolder = LineEdit(self)
        self.lineEpw = LineEdit(self)
        self.lineCases = QLineEdit()
        self.validatorCases = QIntValidator(1, 9999999, self)
        self.lineCases.setValidator(self.validatorCases)

        self.group = QButtonGroup()
        self.lhsRB = QRadioButton("Latin Hypercube Sampling")
        self.randomRB = QRadioButton("Random")
        self.group.addButton(self.randomRB)
        self.group.addButton(self.lhsRB)

        self.gridLayout = QGridLayout()

        self.menuBar = QMenuBar()
        self.help = self.menuBar.addMenu("Ajuda")
        self.helpAction = QAction("Documentação", self)
        self.help.addAction(self.helpAction)
        self.helpAction.triggered.connect(self.documentationClicked)
        self.processingMessage = QLabel()
        self.gridLayout.setMenuBar(self.menuBar)

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
        if len(self.args) > 1:
            pixmap = QPixmap("../media/img/title.png")
        else:
            pixmap = QPixmap("./Images/title.png")
        self.logo.setPixmap(pixmap)

        self.gridLayout.addWidget(self.logo, 0, 0)
        self.gridLayout.addWidget(self.casesButton, 1, 0)
        self.gridLayout.addWidget(self.simulationButton, 2, 0)

        if self.firstTime:
            self.firstTime = False

            self.casesButton.clicked.connect(self.casesButtonClicked)
            self.simulationButton.clicked.connect(self.simulationButtonClicked)
            self.cancelButton.clicked.connect(self.cancelButtonClicked)
            self.confirmButtonCases.clicked.connect(self.confirmButtonCasesClicked)
            self.chooseIdfButton.clicked.connect(self.chooseIdfClicked)
            self.chooseCSVButton.clicked.connect(self.chooseCsvClicked)
            self.chooseFolderButton.clicked.connect(self.chooseFolderClicked)
            self.chooseEpwButton.clicked.connect(self.chooseEpwButtonClicked)
            self.confirmButtonSimulation.clicked.connect(self.confirmButtonSimulationClicked)

            self.setLayout(self.gridLayout)
            self.setFixedSize(650, 250)
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

        idfLabel.setText("Arquivo base IDF:")
        csvLabel.setText("Arquivo de configuração CSV:")
        folderStoreLabel.setText("Pasta para salvar os arquivos IDF's:")
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
        self.gridLayout.addWidget(self.lhsRB, 5, 2, Qt.AlignRight)

        self.gridLayout.addWidget(sampleSize, 6, 0, 1, 2)
        self.gridLayout.addWidget(self.lineCases, 6, 2)

        self.gridLayout.addWidget(self.confirmButtonCases, 7, 0, 1, 3, Qt.AlignTop)
        self.gridLayout.addWidget(self.cancelButton, 8, 0, 1, 3, Qt.AlignTop)

    ##
    ## @brief      This method is actived whenever the "simulationButton" is
    ##             pressed. First of all, it remove all components from
    ##             the window. After that it justs configures labels,
    ##             lineTexts and buttons into the grid layout.
    ##
    ## @param      self  Non static method
    ##
    ## @return     This is a void method
    ##
    def simulationButtonClicked(self):
        self.clearAll()

        folderStoreLabel = QLabel()
        epwLabel =  QLabel()

        folderStoreLabel.setText("Pasta com os arquivos idf's")
        epwLabel.setText("Arquivo EPW")

        self.gridLayout.addWidget(folderStoreLabel, 1, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.chooseFolderButton, 1, 1)
        self.gridLayout.addWidget(self.lineFolder, 1, 2)

        self.gridLayout.addWidget(epwLabel, 2, 0, Qt.AlignRight)
        self.gridLayout.addWidget(self.chooseEpwButton, 2, 1)
        self.gridLayout.addWidget(self.lineEpw, 2, 2)

        # Doing this just to the UI get a little bit more beautiful
        self.gridLayout.addWidget(QLabel(), 3, 0)
        self.gridLayout.addWidget(self.processingMessage, 4, 0, 1, 3, Qt.AlignCenter)

        self.gridLayout.addWidget(self.confirmButtonSimulation, 7, 0, 1, 3, Qt.AlignBottom)
        self.gridLayout.addWidget(self.cancelButton, 8, 0, 1, 3, Qt.AlignBottom)

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
    def confirmButtonCasesClicked(self):
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
    ## @brief      This method is actived whenever the "chooseEpwButton" is
    ##             clicked. When this method is activated, a QFileDialog will
    ##             be show to the user and it will be possible to choose a
    ##             EPW file. After choosed the EPW, the "lineEpw" attribute
    ##             will have its text changed to the absolute path to EPW
    ##             choosed.
    ##
    ## @param      self  Non static method
    ##
    ## @return     This is a void method
    ##
    def chooseEpwButtonClicked(self):
        msg = "Escolha o arquivo EPW"
        epwFile = QFileDialog.getOpenFileName(self, msg, os.getenv("HOME"), filter="*.epw")
        self.setLineEpwText(epwFile[0])

    ##
    ## @brief      This method is called whenever the confirm button of the
    ##             screen of simulation is clicked. This method check if all
    ##             fields are filled. If not, a warning message will appear
    ##             to the user through a MessageBox informing that all fields
    ##             need to be completed. Otherwise, if all fields were filled,
    ##             the simulation will be executed.
    ##
    ## @param      self  Non static method
    ##
    ## @return     This is a void method
    ##
    def confirmButtonSimulationClicked(self):
        msgBox = QMessageBox()
        msgBox.setIcon(QMessageBox.Warning)
        msgBox.setWindowIcon(QIcon(self.pathToIcon))
        msgBox.setWindowTitle("EPlusPlus-WAR")
        msgBox.setText("Todos os campos devem estar preenchidos para prosseguir!")

        if self.lineFolder.text() == "":
            msgBox.exec_()
        elif self.lineEpw.text() == "":
            msgBox.exec_()
        else:
            self.runSimulation()

    ##
    ## @brief      This method is used every time the "Documentation" button
    ##             is clicked at the menu bar. This method open the manual
    ##             of the program in pdf format at the default browser of the
    ##             current user.
    ##
    ## @param      self  Non static method
    ##
    ## @return     This is a void method.
    ##
    def documentationClicked(self):
        if len(self.args) > 1:
            doc = "../docs/documentacaoEPlusPlus.pdf"
        else:
            doc = "./Documents/documentacaoEPlusPlus.pdf"
        webbrowser.open("file://"+os.path.abspath(doc))

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
            self.cancelButtonClicked()
        except ColumnException as e:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("EPlusPlus-ERR")
            msg = "O arquivo csv ou o arquivo idf não estão no formato correto!"
            msgBox.setText(msg)
            msgBox.exec_()
            self.actorUser.removeTemporaryCsv(pathToFolder)

    ##
    ## @brief      At first lines, we transform the content informed by the
    ##             user at the current screen into strings. After that, we
    ##             create a QMessageBox to show important information. Then
    ##             it will try to run the simulation through the "actorUser" (
    ##             see its documentation for more info). If no IDF file be
    ##             founded at the folder informed, a exception will be raised.
    ##             Otherwise, if at least, one IDF be founded, the simulation
    ##             will occur normally.
    ##
    ## @param      self  Non static method
    ##
    ## @return     This is a void method.
    ##
    def runSimulation(self):
        pathToFolder = self.lineFolder.text()
        pathToEpw = self.lineEpw.text()
        msgBox = QMessageBox()
        msgBox.setWindowIcon(QIcon(self.pathToIcon))
        msg = ""

        try:
            self.actorUser.findIdfFiles(pathToFolder)
            msg = "Processando arquivos..."
            self.processingMessage.setText(msg)
            QApplication.processEvents()
            self.actorUser.runSimulation(pathToFolder, pathToEpw)
            msgBox.setIcon(QMessageBox.Information)
            msgBox.setWindowTitle("EPlusPlus-INF")
            msg = "Processo finalizado! Verifique a pasta informada para acessar os arquivos."
            msgBox.setText(msg)
            msgBox.exec_()
            self.cancelButtonClicked()
        except NoIdfException as e:
            msgBox.setIcon(QMessageBox.Critical)
            msgBox.setWindowTitle("EPlusPlus-ERR")
            msg = "Não há nenhum arquivo IDF na pasta informada!"
            msgBox.setText(msg)
            msgBox.exec_()

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
    ## @param      self    Non static method
    ## @param      string  String that will be show at the lineCases
    ##
    ## @return     This is a void method
    ##
    def setLineCasesText(self, string):
        self.lineCases.setText(string)

    ##
    ## @brief      This method sets the second lineText of the 3rd screen
    ##             with the value equals to the string passed as arg.
    ##
    ## @param      self    Non static method
    ## @param      string  String that will be show at the lineEpw
    ##
    ## @return     This is a void method.
    ##
    def setLineEpwText(self, string):
        self.lineEpw.setText(string)

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
        self.setLineEpwText("")
        self.processingMessage.setText("")
        self.group.setExclusive(False)
        self.randomRB.setChecked(False)
        self.lhsRB.setChecked(False)
        self.group.setExclusive(True)