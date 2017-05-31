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

	def generateCases(pathToIdf, pathToCsv, pathToFolder, sampleSize, method):
		dictionary = fileManager.csvToHash(pathToCsv)
		if method == "RANDOM":
			mappedValues = statiscal.randomValues(dictionary, sampleSize)
		elif method == "LHS":
			lhd = statiscal.lhsValues(dictionary, sampleSize)
			mappedValues = statiscal.mapValues(lhd, dictionary, sampleSize)

		fileManager.writeMappedValues(mappedValues, pathToFolder)
		fileManager.writeNewValues(pathToIdf, pathToFolder)