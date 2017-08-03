import sqlite3

##
## @brief      This class is responsible to iterate with the database of the
##             EPlusPlus. The methods are very simple, including create the 
##             database, create the tables, and insert the data in the base.
##             The sqlite3 import is necessary, since we are working with this
##             specific database.
##
class ActorDB(object):
	def __init__(self):
		super(ActorDB, self).__init__()
		self.nameTable = 'simulacao'

	##
	## @brief      This method is very simple. It just creates the database
	##             of our program if not exists and close.
	##
	## @param      self            Non static method
	## @param      pathToDataBase  The path to data base
	##
	## @return     This is a void method.
	##
	def createDataBase(self, pathToDataBase):
		conn = sqlite3.connect(pathToDataBase)
		conn.commit()
		conn.close()		

	##
	## @brief      This method is responsible for create the table in the 
	##             database and to insert all the data from the last simulation.
	##             Its important to explain that for each batch of simulation,
	##             we create a new table. So, for standardize the name of the
	##             tables each table start with the name 'simualcao' 
	##             concatenated with the number of the simulation. Doing this,
	##             the user will be able to compare new and old simulations.
	##             So this function creates a query using the name of the table
	##             concatenated with the number of the simulation and append
	##             a '%s' for each column in the csvHeader. Finally, it will
	##             create a column 'nomeArquivo' that references each 
	##             file was responsible for that results. Then the cursor
	##             just executes the query and we commit and close the 
	##             connection.
	##
	## @param      self            Non static method
	## 
	## @param      pathToDataBase  The path to data base
	## 
    ## @param      header          The header from the csv files result. 
	##                             Obtained from the function 
	##                             'getHeaderFromCsvResult' of the 'fileManager'
	##                             class. See its documentation for more info. 
	##                             
	##
	## @return     This is a void method
	##
	def createTable(self, pathToDataBase, csvHeader):
		firstTime = True
		conn = sqlite3.connect(pathToDataBase)
		cursor = conn.cursor()
		queryTables = """SELECT * FROM sqlite_master WHERE type='table';"""
		tables = list(cursor.execute(queryTables))

		if len(tables) > 0:
			self.nameTable += str(len(tables) + 1) 
		else:
			self.nameTable += str(1)

		createTable = """CREATE TABLE IF NOT EXISTS	%s (""" % (self.nameTable)
		for column in csvHeader:
			if not firstTime:
				createTable += """,'%s' REAL"""
			else:
				firstTime = False
				createTable += """'%s' TEXT"""
		createTable += """, nomeArquivo TEXT)"""

		finalQuery = createTable % (tuple(csvHeader))
		cursor.execute(finalQuery)
		conn.commit()
		conn.close()

	##
	## @brief      This method connects to the database previously created 
	##             and will insert each row in the current table of simulation.
	##             After doing this for all rows, just commit and ends the
	##             connection.
	##
	## @param      self            Non static method
	## @param      pathToDataBase  The path to data base
	## @param      rows            The rows from the csv files result. Obtained
	##                             from the function 'getRowsFromCsvResult' of
	##                             the file manager class. See its documentation
	##                             for more info. 
	##
	## @return     This is a void method
	##
	def insertData(self, pathToDataBase, rows):
		conn = sqlite3.connect(pathToDataBase)
		cursor = conn.cursor()
		query = self.createQueryInsert(cursor)

		for row in rows:
			finalQuery = query % (tuple(row))
			cursor.execute(finalQuery)

		conn.commit()
		conn.close()

	##
	## @brief      At first, this method performs a 'SELECT' into the database
	##             to get the number of rows of our table. The 'SELECT' will be
	##             executed on a table depending of the 'nameTable'.
	##             After that, it will start a for loop concatenating a '%s' for
	##             each column that the function readed from the table. Finally,
	##             it just finalizes the string with a ')' and return the string.
	##
	## @param      self     Non static method
	## @param      cursor   The cursor used to execute actions into the database.
	##
	## @return     Return a query template that will be used to insert new data
	##             into our database.
	##
	def createQueryInsert(self, cursor):
		firstTime = True
		query = """SELECT * FROM %s """ % (self.nameTable)
		templateQuery = """INSERT INTO %s VALUES (""" % (self.nameTable)
		names = cursor.execute(query)

		for name in names.description:
			if not firstTime:
				templateQuery += ",'%s' "
			else:
				templateQuery += "'%s'"
				firstTime = False

		templateQuery += ")"
		return templateQuery

	##
	## @brief      This method is basically a 'main' for this class. It's
	##             responsible for create the database, the table and to 
	##             insert the data.
	##
	## @param      self            Non static method
	## 
	## @param      pathToFolder    The path to folder
	## 
	## @param      header          The header from the csv files result. 
	##                             Obtained from the function 
	##                             'getHeaderFromCsvResult' of the 'fileManager'
	##                             class. See its documentation for more info. 
	##                             
	## @param      rows            The rows from the csv files result. Obtained
	##                             from the function 'getRowsFromCsvResult' of
	##                             the file manager class. See its documentation
	##                             for more info. 
	##
	## @return     This is a void method
	##
	def createAndInsert(self, pathToFolder, header, rows):
		pathToDataBase = pathToFolder + '/' + self.nameTable + '.db'
		self.createDataBase(pathToDataBase)
		self.createTable(pathToDataBase, header)
		self.insertData(pathToDataBase, rows)