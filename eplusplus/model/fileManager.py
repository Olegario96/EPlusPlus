import os
import csv
from eplusplus.exception  import ColumnException

##
## @brier This class is responsible for get the values from the csv file
##        informed by the user and also to write the new values into the idf
##        files. This class transform the values from the csv into a dictionary
##        of lists which list represents a column from the csv, following the
##        order in the csv. The list in each entry has all possible values. This
##        class also writes the "mappedValues" obtained from "mapValues" method
##        of the Statiscal class. The import of the os is used to get the name
##        of the idf file. The csv library is  needed cause we need to open the
##        csv.
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
		newFile = open(pathToFolder + "/tempFile.csv", 'w', newline="")
		csvWriter = csv.writer(newFile, delimiter=',', quotechar='|')

		csvWriter.writerow(self.headerCsv)

		for values in mappedValues:
			csvWriter.writerow(values)

	##
	## @brief      This method is the core of the first use case. This method
	##             reads the temporary csv file and the idf file. After that,
	##             it reads line by line of the csv, which represents a sample.
	##             For each sample, a new idf file will be created. This is
	##             necessary, because each idf represents a case. Next, we
	##             start to iterate line by line of the idf until find the
	##             "@@" sequence, its a specie of a template. We can check
	##             if the "@@" sequence is at the line just checking the first
	##             member (line[0]) and check if the line is not empty to not
	##             have problems with exception. If this condition is not
	##             attended, this means that is just a normal line and we just
	##             have to write it.Finally, we map the value using the "index"
	##             function. The index function receives the element that we are
	##             serching, and returns the position at the list.
	##             The final if is just to bring the comments in the
	##             old the idf to the new. We repeat the process for each
	##             sample (row in the csv).
	##
	## @param      self          Non static method
	## @param      pathToIdf     The path to idf
	## @param      pathToFolder  The path to folder where the new idf files
	##                           will be saved.
	## @param      method        Method of sampling. At the version 1.0 can be
	##                           "LHS" or "RANDOM"
	##
	## @return     This is a void method.
	##
	def writeNewValues(self, pathToIdf, pathToFolder, method):
		idfFile = open(pathToIdf, 'r')
		csvFile = open(pathToFolder + "/tempFile.csv", 'r')

		csvReader = csv.reader(csvFile, delimiter=',')
		nameColumns = csvReader.__next__()

		idfReader = csv.reader(idfFile, delimiter=',')
		idfLines = list(idfReader)

		i = 0
		for row in csvReader:
			if row:
				newFile = pathToFolder + "/" + os.path.basename(pathToIdf[:-4])
				newFile += "_" + method.upper() + "_" + str(i) + ".idf"
				idfOut = open(newFile, 'w')
				for line in idfLines:
					if line:
						if  "@@" in line[0]:
							valueToBeMapped = line[0].replace(" ", "")
							try:
								index = nameColumns.index(valueToBeMapped)
							except Exception as e:
								msg = "Campo do IDF não encontrado no CSV!"
								raise ColumnException(msg)
							newLine = "    "+str(row[index])+","+line[1]+"\n"
						else:
							newLine = line[0]
							if len(line) > 1:
								newLine += "," + line[1] + "\n"
							else:
								newLine += "\n"
					else:
						newLine = "\n"

					idfOut.write(newLine)
				i += 1

	##
	## @brief      Removes a temporary csv.
	##
	## @param      self          Non static method.
	## @param      pathToFolder  The path to folder where the temp file is
	##                           located.
	##
	## @return     This is a void method.
	##
	def removeTemporaryCsv(self, pathToFolder):
		os.remove(pathToFolder + "/tempFile.csv")

	##
	## @brief      This method iterate through each file in the folder passed
	##             as arg. For each file, it will check if is a IDF file 
	##             and has the "LHS" or "RANDOM" string in the name of the file.
	##             If both condition are attended, then will append the file
	##             in a list. At the end, just return the list
	##
	## @param      self          Non static method
	## @param      pathToFolder  The path to folder that has the IDF files
	##
	## @return     Return the IDF files generated by the EPlusPlus in the
	##             "generateCases" method.
	##
	def getIDFFiles(self, pathToFolder):
		idfFiles = []
		files = os.listdir(pathToFolder)
		for file in files:
			lhsOrRandom = "LHS" in str(file) or "RANDOM" in str(file)
			if str(file).endswith(".idf") and lhsOrRandom:
				idfFiles.append(file)

		return idfFiles