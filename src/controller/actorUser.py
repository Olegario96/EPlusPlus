import csv
from eplusplus.model import PlatformManager
from eplusplus.model import FileManager
from eplusplus.model import Statiscal

class ActorUser(object):
	"""docstring for ActorUser"""
	def __init__(self):
		super(ActorUser, self).__init__()
		self.platformManager = PlatformManager()
		self.fileManager = FileManager()
		self.statiscal = Statiscal()

	def generateCases(self, pathToIdf, pathToCsv, pathToFolder, sampleSize, method):
		dictionary = self.fileManager.csvToHash(pathToCsv)
		if method == "RANDOM":
			mappedValues = self.statiscal.randomValues(dictionary, sampleSize)
		elif method == "LHS":
			lhd = self.statiscal.lhsValues(dictionary, sampleSize)
			mappedValues = self.statiscal.mapValues(lhd, dictionary, sampleSize)

		self.fileManager.writeMappedValues(mappedValues, pathToFolder)
		self.fileManager.writeNewValues(pathToIdf, pathToFolder)