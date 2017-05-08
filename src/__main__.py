from eplusplus.model import PlatformManager
from eplusplus.test import TestPlatformManager
from eplusplus.exception import InstallException

testPM = TestPlatformManager()
pM = PlatformManager()
print("test main")
testPM.testCheckAndInstallLinux(pM)