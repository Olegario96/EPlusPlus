##
## @brief      Exception for signaling column errors. This exception is used
##             when the csv supplied by the user doesn't match with the idf
##             file. This exception is raised when the idf file has some value
##             that is not mapped to csv. For example: if the idf file requires
##             "@@ExpPis3@@" the csv file must have a column with this name,
##             otherwise, this exception will raise.
##
class ColumnException(Exception):
	pass