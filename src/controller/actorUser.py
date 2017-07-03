import os
import csv
import subprocess
from eplusplus.model import FileManager
from eplusplus.model import Statiscal
from eplusplus.model import PlatformManager
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
		self.fileManager.removeTemporaryCsv(pathToFolder)

	##
	## @brief      This method lists all files and folders inside the
	##             folder passed as arg. After that, we iterate through
	##             each element. If, at least, one file has the .idf
	##             extenstion, then return True. If no IDF file were
	##             founded, than raise a exception.
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
		files = os.listdir(pathToFolder)
		for file in files:
			if str(file).endswith(".idf"):
				return True

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
	## @param      pathToFolder  The path to folder
	## @param      pathToEpw     The path to epw
	##
	## @return     This is a void method
	##
	def runSimulation(self, pathToFolder, pathToEpw):
		files = os.listdir(pathToFolder)
		if self.platformManager.isLinux():
			for file in files:
				if "LHS" in str(file) or "RANDOM":
					msgBox = QMessageBox()
					absPath = str(pathToFolder) + "/" + str(file)
					output = str(pathToFolder) + "/" + str(file)[:-4]
					cmd = "energyplus -w %s -d %s -r %s" % (pathToEpw, output, absPath)
					subprocess.call(cmd, shell=False)
		elif self.platformManager.isWindows():
			for file in files:
				if "LHS" in str(file) or "RANDOM":
					absPath = str(pathToFolder) +"/" + str(file)
					output = absPath[:-4]
					cmd = ["C:/EnergyPlusV8-7-0/energyplus.exe", "-w"]
					cmdContinue = [pathToEpw, "-d", output, "-r", absPath]
					cmd += cmdContinue
					subprocess.call(cmd)

	##
	## @brief      Removes a temporary csv from the folder where the operations
	##             were made it.
	##
	## @param      self          Non static method.
	## @param      pathToFolder  The path to folder where is the temporary
	##                           CSV file.
	##
	## @return     This is a void method.
	##
	def removeTemporaryCsv(self, pathToFolder):
		self.fileManager.removeTemporaryCsv(pathToFolder)
