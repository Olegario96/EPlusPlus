import unittest
from eplusplus.model.platformManager import PlatformManager

##
## @brief      This class test the main methods from the class "PlatformManager".
##             It check if the tools are installed, and, if don't, it will try
##             to install. If all occurs okay, then will return true and will
##             suceed on the test. Otherwise, will throw and exception and
##             will fail.
##
class TestPlatformManager(unittest.TestCase):

	##
	## @brief      This method test if the tool and installation and if all the
	##             tools are installed correctly on the Linux platform.
	##
	## @param      self  Non static method
	##
	## @param      pM    A object from the class "PlatformManager". Used to
	##                   test it's methods.
	##
	## @return     This is a void function.
	##
	def testCheckAndInstallLinux(self):
		pM = PlatformManager()
		self.assertEqual(pM.checkAndInstall(), True)

	##
	## @brief      This method test if the tool and installation and if all the
	##             tools are installed correctly on the Windows platform.
	##
	## @param      self  Non static method
	##
	## @param      pM    A object from the class "PlatformManager". Used to
	##                   test it's methods.
	##
	## @return     This is a void function.
	##
	def testCheckAndInstallWindows(self):
		pM = PlatformManager()
		self.assertEqual(pM.checkAndInstall(), True)

if __name__ == '__main__':
	unittest.main()