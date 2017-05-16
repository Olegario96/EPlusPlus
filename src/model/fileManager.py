import os
import csv
from eplusplus.exception.columnException import ColumnException

##
## @brier This class is responsible for get the values from the csv file
##        informed by the user and also to write the new values into the idf
##        files. This class transform the values from the csv into a list
##        of lists which list represents a column from the csv, following the
##        order. The import of the os is used to get the name of the idf file.
##        The csv library is needed cause we need to open the csv. The
##        ColumnException is used when the csv and idf file doesn't match
##        (i.e. the idf file require values that are in the csv file.)
##
##
class FileManager(object):

	def __init__(self):
		super(FileManager, self).__init__()

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