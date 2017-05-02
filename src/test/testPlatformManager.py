import unittest
from model.platformManager import PlatformManager

class TestPlatformManager(unittest.TestCase):
	def testCheckAndInstallLinux(self, pM):
		self.assertEqual(pM.checkAndInstall(), True)

