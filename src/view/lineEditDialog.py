import os
from PyQt5.QtWidgets import QLineEdit, QFileDialog

class LineEditDialog(QLineEdit):
	def __init__(self, folder, parent):
		super(LineEditDialog, self).__init__()
		self.folder = folder
		self.parentWindow = parent

	def mousePressEvent(self, event):
		msg = ""
		if not self.folder:
			msg = "Escolha o arquivo idf"
			filename = QFileDialog.getOpenFileName(self.parentWindow, msg, os.getenv("HOME"))
			self.parentWindow.setLineIdfText(filename[0])
		else:
			msg = "Escolha a pasta para salvar os novos arquivos IDF's gerados"
			directory = str(QFileDialog.getExistingDirectory(self.parentWindow, msg, os.getenv("HOME")))
			self.parentWindow.setLineIdfText(directory)

	def keyPressEvent(self, event):
		None

