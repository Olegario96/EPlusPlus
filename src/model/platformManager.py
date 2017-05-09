import os
import subprocess
import platform
from eplusplus.exception.installException import InstallException
from .installer import Installer

##
## @brief      This class creates a simple interface between the eplusplus
##             software and the operating system of the user. Using this class,
##             we can check if all the tools are ready to be used, and, if not,
##             we can install it. The "os" import is used to get the abstolute
##             path to some files and check if a path is a file or not. The
##             "subprocess" we use to create new processes and wait for them.
##             The "platform" library is used to check the OS of the user.
##             Finally we import our personal packages. The class "Installer"
##             is responsible for the installtion of the tools and
##             "InstallException" we just throw. Check their documentation for
##             more info.
##
class PlatformManager(object):

	def __init__(self):
		super(PlatformManager, self).__init__()
		self.installer = Installer()

	##
	## @brief      Determines if the OS of the user is linux or not.
	##
	## @param      self  Non static method.
	##
	## @return     True if linux, False otherwise.
	##
	def isLinux(self):
		return platform.system() == "Linux" or platform.system() == "Linux2"

	##
	## @brief      Determines if the OS of the user is windows or not.
	##
	## @param      self  Non static method.
	##
	## @return     True if windows, False otherwise.
	##
	def isWindows(self):
		return platform.system() == "Windows"

	##
	## @brief      Determines if the OS of the user is osx or not.
	##
	## @param      self  Non static method.
	##
	## @return     True if osx, False otherwise.
	##
	def isOSX(self):
		return platform.system() == "Darwin"

	##
	## @brief      This function check if a tool that we need it is installed
	##             or not on Windows platform. First we check what is the
	##             absolute path to the executable. Next, we check if is a file
	##             , so we can now if the executable is on the machine or not.
	##             If so, then we try to call the program. If all it's okay,
	##             we just kill the program that we call and return true. If
	##             any problem occur, we return false. Otherwise, return false.
	##
	##
	## @param      self  The object
	## @param      exc   Path to the executable
	##
	## @return     Return true if the program is installed on the machine, and
	##             false otherwise.
	##
	def checkToolWindows(self, exc):
		absPath = os.path.abspath(exc)
		if os.path.isfile(absPath):
			try:
				process = subprocess.Popen(exc, shell=True)
				process.kill()
				return True
			except:
				return False
		else:
			return False

	##
	## @brief      Check if the tools that we needed it is installed on the
	##             Linux platform. We just try to call the program. If all
	##             it's okay, then we kill the process that we created, and
	##             return true. False, otherwise.
	##
	## @param      self  Non static method
	## @param      exc   The nome of program on the shell
	##
	## @return     Return true if the tool is installed, false otherwise.
	##
	def checkToolLinux(self, exc):
		try:
			process = subprocess.Popen(exc, shell=True)
			process.kill()
			return True
		except:
			return False

	##
	## @brief      This function check what is the OS of the user. If is not
	##             OSX, neither Linux, neither Windows then return False.
	##             Otherwise, check the tools on the respective platform and
	##             install if needed.
	##
	## @param      self  Non static method
	##
	## @return     Return false if the platform is not Windows, Linux or OSX.
	##             Otherwise, return if the tools are installed.
	##
	def checkAndInstall(self):
		if self.isOSX():
			return self.checkAndInstallOSX()
		elif self.isLinux():
			return self.checkAndInstallLinux()
		elif self.isWindows():
			return self.checkAndInstallWindows()
		else:
			return False

	##
	## @brief      This function check if the EnergyPlus and DB browser for
	##             SQLite are installed. If they aren't, it will try to install.
	##             If any problem occur, the system will stop and ask to the
	##             user manually install the respective tool. The installer
	##             is responsible for the installation. Check it's documentation
	##             for more info. This method was designed to Linux platform.
	##
	## @param      self  Non static method
	##
	## @return     Return true is the tools are already installed or the
	##             installation occur all okay. Otherwise, will throw the
	##             "InstallException"
	##
	def checkAndInstallLinux(self):
		msg = "Please, manually install the following tool: "
		if not self.checkToolLinux("runenergyplus"):
			self.installer.installEplusLinux()
			if not self.checkToolLinux("runenergyplus"):
				msg += "EnergyPlus"
				raise InstallException(msg)

		if not self.checkToolLinux("sqlitebrowser"):
			self.installer.installDBrowserLinux()
			if not self.checkToolLinux("sqlitebrowser"):
				msg += "sqlitebrowser"
				raise InstallException(msg)

		return True

	##
	## @brief      This function check if the EnergyPlus and DB browser for
	##             SQLite are installed. If they aren't, it will try to install.
	##             If any problem occur, the system will stop and ask to the
	##             user manually install the respective tool. The installer
	##             is responsible for the installation. Check it's documentation
	##             for more info. This method was designed to Windows platform.
	##
	## @param      self  Non static method
	##
	## @return     Return true is the tools are already installed or the
	##             installation occur all okay. Otherwise, will throw the
	##             "InstallException"
	##
	def checkAndInstallWindows(self):
		msg = "Please, manually install the following tool: "
		path = "C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"
		if not self.checkToolWindows("C:\EnergyPlusV8-7-0\energyplus.exe"):
			self.installer.installEplusWindows()
			if not self.checkToolWindows("C:\EnergyPlusV8-7-0\energyplus.exe"):
				msg += "EnergyPlusV8-7-0"
				raise InstallException(msg)

		if not self.checkToolWindows(path):
			self.installer.installDBrowserWindows()
			if not self.checkToolWindows(path):
				msg += "sqlitebrowser"
				raise InstallException(msg)

		return True