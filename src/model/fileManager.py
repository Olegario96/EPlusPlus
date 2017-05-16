import os
import csv
from .statiscal import Statiscal
from eplusplus.exception.columnException import ColumnException

##
## @brief
##
class FileManager(object):

	def __init__(self):
		super(FileManager, self).__init__()
		self.statiscal = Statiscal()


	##
	## @brief      This method reads the csv informed by the user. In the
	##             first iteration, just creates a list with 'n' lists where
	##             n is equal to the number of the columns of the csv. In all
	##             other iterations it just apend the respective value of the
	##             column on each list. For example: the values of the first
	##             column will have its values append on the list 0 of the list.
	##             The second column will have its values append on the list 1
	##             of the list and so go on. At the end, just return this
	##             "superlist".
	##
	## @param      self       Non static method
	## @param      pathToCsv  The path to csv informed by the user. The path
	##                        must be absolute.
	##
	## @return     Return the csv and its columns in form of a list of lists.
	##
	def columnsToLists(self, pathToCsv):
		firstTime = True
		csvFile = open(pathToCsv, 'r')
		csvReader = csv.reader(csvFile, delimiter=',', quotechar='|')

		for row in csvReader:
			if not firstTime:
				for element, column in zip(row, columns):
					column.append(element)
			else:
				firstTime = False
				columns = [[] for i in range(len(row))]

		return columns


	##
	## @brief      This method take the columns received from the
	##             "columnsToLists" method and then apply a sampling method
	##             on the the list based on the number of samples. For example
	##             if we have a sample with 5 values and the "numSamples" is
	##             equal to 3, this means that after apply the sampling method
	##             we will have a list with 3 values choosed from the inital
	##             sample.
	##
	## @param      self        Non static method
	## @param      sample     Columns returned from the "columnsToLists"
	##                         method. See its documentation for more info.
	##
	## @param      numSamples  Number of values that the user wants from the
	##                         the sample. If this value is equal to 2, then
	##                         the returned sample will have 2 elements. If 3,
	##                         will return a list of 3 and so go on.
	##
	## @param      method      Method choosed by the user to apply the sampling
	##                         method. In the first version of the eplusplus can
	##                         be just two values: RANDOM or LHS.
	##
	## @return     The values returned from the sampling method applied. The
	##             length of the list must be equal to the "numSamples" value.
	##
	def calculateNewValues(self, sample, numSamples, method):
		for i in range(0, len(sample)):
			if method == "LHS":
				sample[i] = self.statiscal.lhsValues(sample[i], numSamples)
			elif method == "RANDOM":
				sample[i] = self.statiscal.randomValues(sample[i], numSamples)

		return sample

	##TODO
	def writeNewValues(self, sample, pathToCsv, pathToIdf, pathToFolder):
		idfFile = open(pathToIdf, 'r')
		csvFile = open(pathToCsv, 'r')
		nameColumns = (csv.reader(csvFile, delimiter=',')).__next__()
		idfReader = csv.reader(idfFile, delimiter=',')

		for i in range(0, len(sample)):
			nameFile = os.path.splitext(pathToIdf)[0]
			pathToWrite = nameFile + str(i) + ".idf"
			idfFileOut = open(pathToWrite, 'w')

			for row in idfReader:
				if row:
					if "@@" in row[0]:
						try:
							## I really hate to do this, but I forced to do it.
							## This line is used do throw away all content that
							## is after the ';' symbol and eliminate all blank
							## spaces.
							aux = (row[0].split(";")[0]).replace(" ", "")
							index = nameColumns.index(aux)
						except:
							raise ColumnException("Erro! As colunas do csv não são as mesmas solicitadas pelo arquivo idf!")
				else:
					continue