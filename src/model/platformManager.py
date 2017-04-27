import os
import signal
import subprocess
import platform
import exception.installException
from installer import Installer

class PlatformManager(object):
	"""docstring for PlatformManager"""
	def __init__(self):
		super(PlatformManager, self).__init__()
		self.installer = Installer()

	def isLinux(self):
		return platform == "linux" or platform == "linux2"

	def isWindows(self):
		return platform == "win32"

	def isOSX(self):
		return platform == "darwin"

	def checkTool(self, exc):
		try:
			process = subprocess.Popen(exc)
			process.kill()
			return True
		except OSError as error:
			if error.errno == os.errno.ENOENT:
				return False

	def installDBrowser(self):
		pass

	def checkAndInstall(self):
		if self.isOSX():
			self.checkAndInstallOSX()
		elif self.isLinux():
			self.checkAndInstallLinux()
		else:
			self.checkAndInstallWindows()


	def checkAndInstallLinux(self):
		if not self.checkTool("runenergyplys"):
			self.installer.installEplusLinux()
			if not self.checkTool("runenergyplus"):
				raise InstallException("Please, manually install the following tool: EnergyPlus")

		if not self.checkTool("sqlitebrowser"):
			self.installDBrowser()
			if not self.checkTool("sqlitebrowser"):
				raise InstallException("Please, manually install the following tool: sqlitebrowser")