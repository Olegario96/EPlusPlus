import os
import subprocess
import urllib.request
import shutil

class Installer(object):
	"""docstring for Installer"""
	def __init__(self):
		super(Installer, self).__init__()

	def installEplusLinux(self):
		subprocess.call("./scripts/installEplus.sh", shell=True)

	def installDBrowserLinux(self):
		subprocess.call("./scripts/installDBrowser.sh", shell=True)

	def installEplusWindows(self):
		url = "https://github.com/NREL/EnergyPlus/releases/download/v8.7.0/Energyplus-8.7.0-78a111df4a-Windows-x86_64.exe"
		fileName = "EnergyPlusInstaller.exe"
		with urllib.request.urlopen(url) as response, open(fileName, "wb") as outFile:
			shutil.copyfileobj(response, outFile)

		path = os.path.abspath(fileName)
		subprocess.call(path, shell=True)


	def installDBrowserWindows(self):
		url = "https://github.com/sqlitebrowser/sqlitebrowser/releases/download/v3.9.1/DB.Browser.for.SQLite-3.9.1-win64.exe"
		fileName = "sqlitebrowserInstaller.exe"
		with urllib.request.urlopen(url) as response, open(fileName, "wb") as outFile:
			shutil.copyfileobj(response, outFile)

		path = os.path.abspath(fileName)
		subprocess.call(path, shell=True)
