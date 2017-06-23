from distutils.core import setup
from glob import glob
import os
import py2exe
import pyDOE

VERSION=1.0

includes = [
	"sip",
	"PyQt5",
	"PyQt5.QtCore",
	"PyQt5.QtGui",
	"PyQt5.QtWidgets",
	"scipy.linalg.cython_blas",
	"scipy.linalg.cython_lapack",
	"pyDOE"
]

platforms = ["C:\\Python34\\Lib\\site-packages\\PyQt5\\plugins" +
		"\\platforms\\qwindows.dll"]

dll = ["C:\\windows\\syswow64\\MSVCP100.dll",
		"C:\\windows\\syswow64\\MSVCR100.dll"]

images = ["C:\\Users\\GUSTAVO\\EPlusPlus\\media\\img\\title.png",
            			"C:\\Users\\GUSTAVO\\EPlusPlus\\media\\img\\icon.png"]

documents = ["C:\\Users\\GUSTAVO\\EPlusPlus\\docs\\Documento"+
				"documentacaoEPlusPlus.pdf"]

datafiles = [("platforms", platforms),
             ("", dll),
             ("Images", images),
             ("Documents", documents)]

imageformats = glob("C:\\Python34\\Lib\\site-packages\\PyQt5\\"+
			"plugins\\imageformats\\*")

datafiles.append(("imageformats", imageformats))

setup(
	name="eplusplus",
	version=VERSION,
	packages=["eplusplus"],
	url="",
	license="",
	windows=[{"script": "eplusplus/__main__.py"}],
	scripts=[],
	data_files = datafiles,
	options={
		"py2exe": {
			"includes": includes,
		}
	}
)
