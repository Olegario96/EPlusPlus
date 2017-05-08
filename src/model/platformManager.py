import os
import signal
import subprocess
import platform
from eplusplus.exception.installException import InstallException
from .installer import Installer

class PlatformManager(object):
	"""docstring for PlatformManager"""
	def __init__(self):
		super(PlatformManager, self).__init__()
		self.installer = Installer()

	def isLinux(self):
		return platform.system() == "Linux" or platform.system() == "Linux2"

	def isWindows(self):
		return platform.system() == "Windows"

	def isOSX(self):
		return platform.system() == "Darwin"

	def checkTool(self, exc):
		try:
			process = subprocess.Popen(exc, shell=True)
			process.kill()
			return True
		except OSError as error:
			if error.errno == os.errno.ENOENT:
				return False


	def checkAndInstall(self):
		if self.isOSX():
			return self.checkAndInstallOSX()
		elif self.isLinux():
			return self.checkAndInstallLinux()
		else:
			return self.checkAndInstallWindows()


	def checkAndInstallLinux(self):
		if not self.checkTool("runenergyplus"):
			self.installer.installEplusLinux()
			if not self.checkTool("runenergyplus"):
				raise InstallException("Please, manually install the following tool: EnergyPlus")

		if not self.checkTool("sqlitebrowser"):
			self.installer.installDBrowserLinux()
			if not self.checkTool("sqlitebrowser"):
				raise InstallException("Please, manually install the following tool: sqlitebrowser")

		return True

	def checkAndInstallWindows(self):
		if not self.checkTool("C:\EnergyPlusV8-7-0\energyplus.exe"):
			self.installer.installEplusWindows()
			if not self.checkTool("C:\EnergyPlusV8-7-0\energyplus.exe"):
				raise InstallException("Please, manually install the following tool: EnergyPlus")

		if not self.checkTool("C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"):
			self.installer.installDBrowserWindows()
			if not self.checkTool("C:\Program Files\DB Browser for SQLite\DB Browser for SQLite.exe"):
				raise InstallException("Please, manually install the following tool: sqlitebrowser")

		return True

