##
## @brief      Exception for signaling install errors.
##             This exception is thrown whenever the eplusplus try to install
##             some tool like the EnergyPlus or the DB browser for SQLite and
##             didn't achieve the sucess.
##
class InstallException(Exception):
	pass