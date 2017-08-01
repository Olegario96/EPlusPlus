##
## @brief      Class(exception) for idf not formatted. This class is
##             used to signal that no csv was found during the insertion
##             of data into the database. When  this occurs, this means
##             that the simulation in the energyplus have a problem. In
##             other words, the Idf has a problem.
##
class IdfNotFormatted(Exception):
	pass