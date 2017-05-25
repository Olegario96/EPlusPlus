import os
import csv
from eplusplus.exception.columnException import ColumnException

##
## @brier This class is responsible for get the values from the csv file
##        informed by the user and also to write the new values into the idf
##        files. This class transform the values from the csv into a dictionary
##        of lists which list represents a column from the csv, following the
##        order. The list in each entry has all possible values. The import of
##        the os is used to get the name of the idf file. The csv library is
##        needed cause we need to open the csv. The ColumnException is used when
##        the csv and idf file doesn't match (i.e. the idf file require values
##        that are in the csv file.)
##
##
class FileManager(object):

	def __init__(self):
		super(FileManager, self).__init__()


	##
	## @brief      This method creates a dictionary based on the CSV file. Each
	##             entry maps to a list. In the first iteration we create a
	##             entry on the dictionary to represent the variable. In all
	##             other iterations we check if the value is in the list that
	##             represent that variable. If not, we append the new value.
	##             At the end, we have a Hash that map each variable to a list
	##             with respctives all possible values.
	##
	##
	## @param      self       Non static method
	## @param      pathToCsv  The path to csv
	##
	## @return     A dictionary (i.e. Hash table) with the number of entries
	##             equal to the number of variables. Each entry maps to a list
	##             containing all values possible values of that variable
	##
	def csvToHash(self, pathToCsv):
		firstTime = True
		i = 0
		possibleValues = {}
		csvFile = open(pathToCsv, 'r')
		csvReader = csv.reader(csvFile, delimiter=',', quotechar='|')

		for row in csvReader:
			while i < len(row):
				if not firstTime:
					if row[i] not in possibleValues[i]:
						possibleValues[i].append(row[i])
				else:
					possibleValues[i] = []
				i += 1

			firstTime = False
			i = 0

		return possibleValues

	##TODO
	def writeNewValues(self, sample, pathToCsv, pathToIdf, pathToFolder):
		idfFile = open(pathToIdf, 'r')
		csvFile = open(pathToCsv, 'r')
		nameColumns = (csv.reader(csvFile, delimiter=',')).__next__()
		idfReader = csv.reader(idfFile, delimiter=',')

		for i in range(0, len(sample)):
			nameFile = os.path.splitext(pathToIdf)[0]
			pathToWrite = nameFile + str(i) + ".idf"
			#idfFileOut = open(pathToWrite, 'w')

			for row in idfReader:
				if row:
					if "@@" in row[0]:
						try:
							# I really hate to do this, but I forced to do it.
							# This line is used do throw away all content that
							# is after the ';' symbol and eliminate all blank
							# spaces.
							aux = (row[0].split(";")[0]).replace(" ", "")
							index = nameColumns.index(aux)
							print(index)
						except:
							msg = "Erro! As colunas do csv não são as mesmas"
							msg += " solicitadas pelo arquivo idf!"
							raise ColumnException(msg)
				else:
					continue