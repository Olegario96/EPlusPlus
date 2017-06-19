import os
import csv
from eplusplus.model import FileManager
from eplusplus.model import Statiscal
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
		files = os.listidr(pathToFolder)
		for file in files:
			if str(file).endswith(".idf"):
				return True

		msg = "Não existe nenhum arquivo IDF na pasta informada!"
		raise NoIdfException(msg)

	def runSimulation(self, pathToFolder, pathToEpw):
		pass