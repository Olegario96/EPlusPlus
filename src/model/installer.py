import os
import subprocess

class Installer(object):
	"""docstring for Installer"""
	def __init__(self):
		super(Installer, self).__init__()

	def installEplusLinux(self):
		subprocess.call("../scripts/installEplus.sh", shell=True)

