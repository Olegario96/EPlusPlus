import os
import csv
import subprocess
from .actorDB import ActorDB
from eplusplus.model import FileManager
from eplusplus.model import Statiscal
from eplusplus.model import PlatformManager
from eplusplus.model import ProcessManager
from eplusplus.exception import NoIdfException

##
## @brief      This class represents the controller of the application.
##             This class is reponsible for execute the actions requested
##             by the user through the UI. At the first version of the
##             eplusplus, the basic methods are generate the cases and
##             run the simulation.
##
class ActorUser(object):
	def __init__(self):
		super(ActorUser, self).__init__()
		self.fileManager = FileManager()
		self.statiscal = Statiscal()
		self.platformManager = PlatformManager()
		self.procesManager = ProcessManager()
		self.actorDB = ActorDB() 

	##
	## @brief      This method will check what is the OS that is running on
	##             the machine. After that, will check if both tools are
	##             installed on the computer. If not, return false. True,
	##             otherwiser.
	##
	## @param      self  Non static method.
	##
	## @return     Return if the current machine has EnergyPlus and SQLiteBrowser
	##             installed.
	##
	def checkTools(self):
		if self.platformManager.isLinux():
			hasEnergyPlus = self.platformManager.checkToolLinux("runenergyplus")
			hasSQLiteBrowser = self.platformManager.checkToolLinux("sqlitebrowser")
			return hasEnergyPlus and hasSQLiteBrowser
		if self.platformManager.isWindows():
			pathEplus = "C:\EnergyPlusV8-7-0\energyplus.exe"
			pathSQLiteBrowser = "C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"
			hasEnergyPlus = self.platformManager.checkToolLinux(pathEplus)
			hasSQLiteBrowser = self.platformManager.checkToolLinux(pathSQLiteBrowser)
			return hasEnergyPlus and hasSQLiteBrowser

	##
	## @brief      Check "checkAndInstall"'s documentation method of the
	##             class "ActorUser" for more information.
	##
	## @param      self  Non static method.
	##
	## @return     This is a void method.
	##
	def checkAndInstall(self):
		self.platformManager.checkAndInstall()

	##
	## @brief      This method receives all parameters through UI.
	##             We don't need to check each value of the args, because
	##             this was already made at the UI. Depending of the method
	##             , the respective sampling method will be called. If the
	##             "LHS" method was choosed, the interpolation of values
	##             will be calculated too. Next, we save the values into a
	##             temporary csv file and write the new idf files. At the
	##             end, we delete the temporary csv file.
	##
	## @param      self          Non static method.
	## @param      pathToIdf     The path to idf file informed through UI.
	## @param      pathToCsv     The path to csv file informed through UI.
	## @param      pathToFolder  The path to folder where the new idf's
	##                           file will be saved. Also informed through
	##                           UI.
	## @param      sampleSize    The sample of size requested by the user.
	##                           Informed through UI.
	## @param      method        The method of sampling. Informed through
	##                           UI.
	##
	## @return     This is a void method.
	##
	def generateCases(self, pathToIdf, pathToCsv, pathToFolder, sampleSize, method):
		dictionary = self.fileManager.csvToHash(pathToCsv)
		if method == "RANDOM":
			mappedValues = self.statiscal.randomValues(dictionary, sampleSize)
		elif method == "LHS":
			lhd = self.statiscal.lhsValues(dictionary, sampleSize)
			mappedValues = self.statiscal.mapValues(lhd, dictionary, sampleSize)

		self.fileManager.writeMappedValues(mappedValues, pathToFolder)
		self.fileManager.writeNewValues(pathToIdf, pathToFolder, method)

	##
	## @brief      This method uses the 'getIDFFiles' if exists
	##             , at least, one Idf file in the folder.
	##
	## @param      self          Non static method
	## @param      pathToFolder  Path to the folder containing the IDF
	##                           files, informed by the user through the
	##                           run simulation screen.
	##
	##
	## @return     Return True if at least one IDF file were founded.
	##             Otherwise, will raise a exception.
	##
	def findIdfFiles(self, pathToFolder):
		idfFiles = self.fileManager.getIDFFiles(pathToFolder)
		if idfFiles:
			return True
		else:
			msg = "Não existe nenhum arquivo IDF na pasta informada!"
			raise NoIdfException(msg)

	##
	## @brief      This method execute the simulation using IDF files and
	##             the EPW file informed by the user. For each IDF file inside
	##             the folder informed by the user, a simulation of the EnergyPlus
	##             will be executed using the EPW file. It has different
	##             commands depending of the operating system. The "-d" argument
	##             is used to create a new folder to each case.
	##
	## @param      self          Non static method.
	## @param      pathToFolder  Path to the folder containing the IDF
	##                           files, informed by the user through the
	##                           run simulation screen.
	## @param      pathToEpw     The path to epw file informed through UI.
	##
	## @return     This is a void method
	##
	def runSimulation(self, pathToFolder, pathToEpw):
		self.procesManager.executeTasks(self.platformManager, pathToEpw, pathToFolder, self.fileManager)

	##
	## @brief      This method gets the header from the csv file. This allow us
	##             to create tables with dynamic names. After that, it takes
	##             the rows from each csv of result generated during the
	##             simulation and finnaly insert all the data into the
	##             database.
	##
	## @param      self          Non static method
	## @param      pathToFolder  The path where is the IDF files generated
	##                           in the 'generateCases' method. Obtained
	##                           from the user through GUI.
	##
	## @return     This is a void method
	##
	def insertIntoDatabase(self, pathToFolder):
		header = self.fileManager.getHeaderFromCsvResult(pathToFolder)
		rows = self.fileManager.getRowsFromCsvResult(pathToFolder)
		self.actorDB.createAndInsert(pathToFolder, header, rows)

	##
	## @brief      This method is used to test if the file of the check box
	##             exists. The first window of the program inform the user
	##             about the white space problem in the path and the user
	##             has the posibility to never see this warning again. So,
	##             to do that, we need to create a persistent solution. 
	##             Then the file manager will test if the file 'checkbox.txt'
	##             exists or not. If not, return false. True, otherwise.
	##
	## @param      self  Non static method.
	##
	## @return     True if exists file, False otherwise.
	##
	def existsFileConfirmCheckBox(self):
		return self.fileManager.existsFileConfirmCheckBox()

	##
	## @brief      It the file didn't exist before and the the user
	##             marked the check box, the file manager will create.
	##
	## @param      self  Non static method.
	##
	## @return     This is a void function.
	##
	def createFileConfirmCheckBox(self):
		self.fileManager.createFileConfirmCheckBox()

	##
	## @brief      Removes directories from the simulation.
	##
	## @param      self          Non static method
	## @param      pathToFolder  The path to folder where lies
	##                           the directories generated during the
	##                           simulation
	##
	## @return     This is a void method.
	##
	def removeDirectories(self, pathToFolder):
		self.fileManager.removeDirectories(pathToFolder)