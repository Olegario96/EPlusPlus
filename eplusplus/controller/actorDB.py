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
		self.nameDataBase = "simulacaoEPlusPlus"
		self.nameTableCases = "casos"
		self.nameTableSimulation = "resultadosSimulacao"
		self.nameTableSample = "amostraSimulacao"

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
	## @brief      Creates table cases in the database. The table have just
	##             one column of the type INTEGER AUTOINCREMENT to indicate the
	##             number of the case
	##
	## @param      self            Non static method
	## @param      pathToDataBase  The path to data base
	##
	## @return     This is a void method
	##
	def createTableCases(self, pathToDataBase):
		conn = sqlite3.connect(pathToDataBase)
		cursor = conn.cursor()

		queryCreate = """CREATE TABLE IF NOT EXISTS casos (
							idCaso  INTEGER PRIMARY KEY AUTOINCREMENT);"""

		cursor.execute(queryCreate)
		conn.commit()
		conn.close()

	##
	## @brief      Creates a table for the results or for the sample. This
	##             method starts creating a connection with the database and
	##             listing all the tables on the  base. If there is more than
	##             3, means that the base already exists, then we need to
	##             set the name of our tables to "len(tables)/3 + 1". Otherwise,
	##             will set with number, which represents the first simulation.
	##             After that, it just creates the query using the 'idCaso'
	##             as FK. At the end, just executes the query to create the
	##             table and commit the changes.
	##
	## @param      self            Non static method
	## @param      pathToDataBase  The path to data base
	## @param      header          The header of the csv that we want create a 
	##                             table
	## @param      typeTable       The type table (i.e. if is of the type 
	##                             'simulation' or 'sample')
	##
	## @return     This is a void function
	##
	def createTableRS(self, pathToDataBase, header, typeTable):
		firstTime = True
		conn = sqlite3.connect(pathToDataBase)
		cursor = conn.cursor()
		queryTables = """SELECT * FROM sqlite_master WHERE type='table';"""
		tables = list(cursor.execute(queryTables))

		if len(tables) > 3:
			if typeTable == "simulation":
				self.nameTableSimulation += str(int((len(tables))/3) + 1) 
				nameTable = self.nameTableSimulation
			elif typeTable == "sample":
				self.nameTableSample += str(int((len(tables))/3) + 1)
				nameTable = self.nameTableSample
		else:
			if typeTable == "simulation":
				self.nameTableSimulation += str(1)
				nameTable = self.nameTableSimulation
			elif typeTable == "sample":
				self.nameTableSample += str(1)
				nameTable = self.nameTableSample

		createTable = """CREATE TABLE IF NOT EXISTS	%s (""" % (nameTable)
		for column in header:
			if not firstTime:
				createTable += """,'%s' REAL"""
			else:
				firstTime = False
				createTable += """idCaso INTEGER"""
				createTable += """,'%s' TEXT"""

		createTable += """, FOREIGN KEY(idCaso) REFERENCES casos(idCaso));"""

		finalQuery = createTable % (tuple(header))
		cursor.execute(finalQuery)
		conn.commit()
		conn.close()

	##
	## @brief      This method is responsible for insert the data of the sample
	##             file and the results obtained from the csv files after 
	##             the simulation process into the database. After connect
	##             in the database, it will create 2 templates of query. One
	##             for the 'simulation' table and other for the the 'sample'
	##             table. Next, it will analyze what is the number of the last
	##             case that was inserted into the database, if no data was
	##             there, then will initiate the variable with 1. Finally 
	##             will insert all results of each sample in the database always
	##             after create a new case. At the end, just commit the changes
	##             and close the connection.
	##
	## @param      self            Non static method
	## @param      pathToDataBase  The path to data base
	## @param      rowsResult      The rows obtained from the result file
	## @param      rowsSample      The rows obtained from the sample file
	##
	## @return     This is a void method
	##
	def insertData(self, pathToDataBase, rowsResult, rowsSample):
		conn = sqlite3.connect(pathToDataBase)
		cursor = conn.cursor()
		querySimulation = self.createQueryInsert(cursor, "simulation")
		querySample = self.createQueryInsert(cursor, "sample")

		case = cursor.execute("""SELECT COUNT (*) FROM casos""")
		idCase = cursor.fetchone()[0]
		if idCase == 0:
			idCase = 1
		else:
			idCase += 1

		for sample in rowsSample:
			cursor.execute("""INSERT INTO casos DEFAULT VALUES;""")
			finalQuerySample = querySample % (tuple([idCase] + sample))
			cursor.execute(finalQuerySample)

			for result in rowsResult:
				finalQuerySimulation = querySimulation % (tuple([idCase] + result))
				cursor.execute(finalQuerySimulation)

			idCase += 1
			
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
	def createQueryInsert(self, cursor, table):
		firstTime = True

		if table == "simulation":
			nTable = self.nameTableSimulation
		elif table == "cases":
			nTable = self.nameTableCases
		elif table == "sample":
			nTable = self.nameTableSample

		query = """SELECT * FROM %s """ % (nTable)
		templateQuery = """INSERT INTO %s VALUES(""" % (nTable) 

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
	## @brief      This method just resets the name of the tables, since each 
	##             time we insert data on the DB after the simulation we create
	##             new tables based on this names.
	##
	## @param      self  Non static method
	##
	## @return     This is a void method.
	##
	def resetTableNames(self):
		self.nameTableSimulation = "resultadosSimulacao"
		self.nameTableSample = "amostraSimulacao"

	def createAndInsert(self, pathToFolder, headerResult, rowsResult, headerSample, rowsSample):
		pathToDataBase = pathToFolder + '/' + self.nameDataBase + '.db'
		self.createDataBase(pathToDataBase)
		self.createTableCases(pathToDataBase)
		self.createTableRS(pathToDataBase, headerResult, "simulation")
		self.createTableRS(pathToDataBase, headerSample, "sample")
		self.insertData(pathToDataBase, rowsResult, rowsSample)
		self.resetTableNames()