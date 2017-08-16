import os
import csv
import shutil
from eplusplus.exception  import ColumnException
from eplusplus.exception import NoCsvException

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
		newFile = open(pathToFolder + "/sample.csv", 'w', newline="")
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
		csvFile = open(pathToFolder + "/sample.csv", 'r')

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

	##
	## @brief      This method gets the header from the csv's result AKA:
	##             'eplusout.csv'. This method is necessary to generate
	##             dynamic names for the columns in the Database. This
	##             method list the files and directories in the folder
	##             of the csv. After that, test if each member of the
	##             list is a directory. If so, will search in this 
	##             folder for the 'eplusout.csv' file. When finds this
	##             file, get the header from the csv and break the 
	##             loops. If the method not find the csv file, this
	##             means that an error occurred during the energyplus
	##             simulation, then, a exception will be thrown.
	##
	## @param      self          Non static method
	## @param      pathToFolder  The path to folder containing the IDF files.
	##
	## @return     The header from csv containing the name of the columns. Can
	##             Throw a exception saying that no CSV was found and a
	##             error occurred during the simulation.
	##
	def getHeaderFromCsvResult(self, pathToFolder):
		header = []
		directories = os.listdir(pathToFolder)
		directories = [pathToFolder +'/' + directory for directory in directories]
		for directory in directories:
			lhsOrRandom = "LHS" in str(directory) or "RANDOM" in str(directory)
			if os.path.isdir(directory) and lhsOrRandom:
				files = os.listdir(directory)
				for file in files:
					if str(file).endswith('eplusout.csv'):
						with open(directory + '/' + file, 'r') as csvFile:
							csvReader = csv.reader(csvFile, delimiter=',')
							header = csvReader.__next__()
							csvFile.close()
							break
				break

		if not header:
			msg = 'Não foi possível encontrar o csv para inserir no banco'
			msg += ' de dados! Por favor, verifique se o IDF não possui objetos'
			msg += ' expandidos ou algum outro erro de formatação.'
			raise NoCsvException(msg)
		else:
			return header

	##
	## @brief      This method is very similar to the 'getHeaderFromCsvResult'
	##             but instead of takes the header from the csv, it takes all
	##             the rows from the csv results from all simulations. After
	##             that, just return the rows in a list of lists in each 
	##             list represents a row.
	##
	## @param      self          Non static method.
	## @param      pathToFolder  The path to folder containing the IDF files.
	##
	## @return     The rows from csv result.
	##
	def getRowsFromCsvResult(self, pathToFolder):
		rows = []
		directories = os.listdir(pathToFolder)
		directories = [pathToFolder +'/' + directory for directory in directories]
		for directory in directories:
			lhsOrRandom = "LHS" in str(directory) or "RANDOM" in str(directory)
			if os.path.isdir(directory) and lhsOrRandom:
				files = os.listdir(directory)
				for file in files:
					if str(file).endswith('eplusout.csv'):
						with open(directory + '/' + file, 'r') as csvFile:
							csvReader = csv.reader(csvFile, delimiter=',')
							csvReader.__next__()
							for row in csvReader:
								rows.append(row + [csvFile.name])
							csvFile.close()

		return rows

	##
	## @brief      Determines if the file 'checkbox.txt' exists or not.
	##
	## @param      self  Non static method.
	##
	## @return     True if exists file, False otherwise.
	##
	def existsFileConfirmCheckBox(self):
		return os.path.isfile('checkbox.txt')

	##
	## @brief      Creates the file to remember the user marked the checkbox
	##             before.
	##
	## @param      self  Non static method
	##
	## @return     This is a void function
	##
	def createFileConfirmCheckBox(self):
		fileCheckBox = open('checkbox.txt', 'w')
		fileCheckBox.write('Now the file exsits.')
		fileCheckBox.close()

	##
	## @brief      This method removes the directories generated
	##             during the simulation. It will remove the folder with
	##             all content inside. The method just check if the folder
	##             was generated by the simulation and remove it.
	##
	## @param      self          Non static method
	## @param      pathToFolder  The path to folder
	##
	## @return     This is a void method.
	##
	def removeDirectories(self, pathToFolder):
		directories = os.listdir(pathToFolder)
		directories = [pathToFolder +'/' + directory for directory in directories]
		for directory in directories:
			lhsOrRandom = "LHS" in str(directory) or "RANDOM" in str(directory)
			if os.path.isdir(directory) and lhsOrRandom:
				shutil.rmtree(directory)