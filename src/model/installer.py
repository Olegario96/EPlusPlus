import os
import subprocess
import urllib

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
		filename = "EnergyPlusInstaller.exe"
		urllib.request.urlretrieve(url, filename)
		path = os.path.abspath("EnergyPlusInstaller.exe")
		subprocess.call([path])

	def installDBrowserWindows(self):
		url = "https://github.com/sqlitebrowser/sqlitebrowser/releases/download/v3.9.1/DB.Browser.for.SQLite-3.9.1-win64.exe"
		filename = "sqlitebrowserInstaller.exe"
		urllib.urlretrieve(url, filename)
		path = os.path.abspath("sqlitebrowserInstaller.exe")
		subprocess.call([path])
