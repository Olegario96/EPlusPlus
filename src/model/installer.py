import os
import subprocess
import urllib.request
import shutil

##
## @brief      This class is responsible for implements the methods that install
##             the tools necessary to the eplusplus. In the initial version,
##             it's only implements the methods to install on Windows and Linux
##             platforms. If we have enough time, we will implement the
##             functions also for the Mac platform. The "os" import is used
##             to get the absolute paths to some files. "Subprocess" is needed
##             to create subprocess and wait for they return. The libraries
##             "urllib.request" and "shutil" are used to download files and
##             copy binary data to a new file, respectively.
##
class Installer(object):

	def __init__(self):
		super(Installer, self).__init__()

	##
	## @brief      This function creates a subprocess responsible to execute
	##             the bash script that installs the EnergyPlus tool. The
	##             script lies on the "scripts" folder and the method just ends
	##             when the installation is concluded. This function was designed
	##             to the Linux platforms.OBS: when the eplusplus
	##             program is running to install the tools, it must be with
	##             root permision, since the installtion of EnergyPlus needs
	##             of the root permission.
	##
	## @param      self  Non static method
	##
	## @return     This is a void method
	##
	def installEplusLinux(self):
		subprocess.call("./scripts/installEplus.sh", shell=False)

	##
	## @brief      This function creates a subprocess responsible to execute
	##             the bash script that installs the DB browser for SQLite tool.
	##             The script lies on the "scripts" folder and the method just
	##             ends when the installation is concluded. This function was
	##             designed to the linux platforms.OBS: when the eplusplus
	##             program is running to install the tools, it must be with
	##             root permision, since the installtion of DB browser for
	##             SQLite needs of the root permission.
	##
	## @param      self  Non static method
	##
	## @return     This is a void function.
	##
	def installDBrowserLinux(self):
		subprocess.call("./scripts/installDBrowser.sh", shell=True)

	##
	## @brief      This function was designed for Windows platform. This
	##             function acess the url of repository where is the executable
	##             file of the installer of the EnergyPlus and create a binary
	##             file called "EnergyPlusInstaller.exe" where writes the
	##             content that was read from the repository. Then, we create
	##             a process do proced with the installation. The method just
	##             ends when the installation is concluded.
	##
	## @param      Non static method
	##
	## @return     This is a void function
	##
	def installEplusWindows(self):
		url = "https://github.com/NREL/EnergyPlus/releases/download/v8.7.0/"
		url += "Energyplus-8.7.0-78a111df4a-Windows-x86_64.exe"
		fileName = "EnergyPlusInstaller.exe"
		with urllib.request.urlopen(url) as response, open(fileName, "wb") as outFile:
			shutil.copyfileobj(response, outFile)

		path = os.path.abspath(fileName)
		subprocess.call(path, shell=False)

	##
	## @brief      This function was designed for Windows platform. This
	##             function acess the url of repository where is the executable
	##             file of the installer of the DB browser for SQLite and create
	##             a binary file called "EnergyPlusInstaller.exe" where writes
	##             the content that was read from the repository. Then, we
	##             create a process do proced with the installation. The method
	##             just ends when the installation is concluded.
	##
	## @param      Non static method
	##
	## @return     This is a void function
	##
	def installDBrowserWindows(self):
		url = "https://github.com/sqlitebrowser/sqlitebrowser/releases/"
		url += "download/v3.9.1/DB.Browser.for.SQLite-3.9.1-win64.exe"
		fileName = "sqlitebrowserInstaller.exe"
		with urllib.request.urlopen(url) as response, open(fileName, "wb") as outFile:
			shutil.copyfileobj(response, outFile)

		path = os.path.abspath(fileName)
		subprocess.call(path, shell=False)