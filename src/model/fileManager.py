import os
import csv
from eplusplus.exception import ColumnException

##
## @brier This class is responsible for get the values from the csv file
##        informed by the user and also to write the new values into the idf
##        files. This class transform the values from the csv into a dictionary
##        of lists which list represents a column from the csv, following the
##        order in the csv. The list in each entry has all possible values. This
##        class also writes the "mappedValues" obtained from "mapValues" method
##        of the Statiscal class. The import of the os is used to get the name
##        of the idf file. The csv library is  needed cause we need to open the
##        csv. The ColumnException is used when the csv and idf file doesn't
##        match (i.e. the idf file require values that are in the csv file.)
##
##
class FileManager(object):

	def __init__(self):
		super(FileManager, self).__init__()
		headerCsv = []

	##
	## @brief      This method creates a dictionary based on the CSV file. Each
	##             entry maps to a list. In the first iteration we create a
	##             entry on the dictionary to represent the variable and we
	##             store the "header" in the atribute of this class. We will use
	##             this value at the "writeMappedValues" later (see its
	##             documentation). In all other iterations we check if the value
	##             is in the list that represent that variable. If not, we
	##             append the new value. At the end, we have a Hash that map
	##             each variable to a list with respctives all possible values.
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
					self.headerCsv = row
					possibleValues[i] = []
				i += 1

			firstTime = False
			i = 0

		return possibleValues

	##
	## @brief      This function writes the sampling in a csv file. It creates
	##             a temporary file in the same folder that the idf files will
	##             be created. Later, the csv file will be removed. Also,
	##             this function writes the "header" of the original csv in the
	##             new.
	##
	## @param      self          Non static method.
	## @param      mappedValues  The mapped values obtained from the method
	##                           "mapValues" in the "Statistical" class. See
	##                           its documentation for more info.
	##
	## @param      pathToFolder  The path to the folder where the file will
	##                           be saved.
	##
	## @return     This is a void method
	##
	def writeMappedValues(self, mappedValues, pathToFolder):
		newFile = open(pathToFolder + "/tempFile.csv", 'w')
		csvWriter = csv.writer(newFile, delimiter=',', quotechar='|')

		csvWriter.writerow(self.headerCsv)

		for values in mappedValues:
			csvWriter.writerow(values)

	##TODO
	def writeNewValues(self, pathToIdf, pathToFolder, method):
		idfFile = open(pathToIdf, 'r')
		csvFile = open(pathToFolder + "/tempFile.csv", 'r')

		csvReader = csv.reader(csvFile, delimiter=',')
		nameColumns = csvReader.__next__()

		i = 0
		for row in csvReader:
			newNameFile = pathToIdf[:-4] + "_" + method.upper() + "_" + str(i)
			idfOut = open(newNameFile, 'w')
			lines = idfFile.readlines()
			for line in lines:
				if line and "@@" in line[0]:
					valueToBeMapped = line[0].replace(" ", "")
					try:
						index = nameColumns.index(valueToBeMapped)
						newLine = "    " + str(row[index])
						if len(line) > 1:
							newLine += line[1]
						idfOut.write(newLine)
					except Exception as e:
						msg = "Erro! As colunas do csv não são as mesmas"
						msg += " solicitadas pelo arquivo idf!"
						raise ColumnException(msg)
				else:
					idfOut.write(line)

			i += 1

	def removeTemporaryCsv(self, pathToFolder):
		os.remove(pathToFolder + "/tempFile.csv")