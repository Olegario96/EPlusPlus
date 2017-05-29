import os
from PyQt5.QtWidgets import QLineEdit, QFileDialog

class LineEditDialog(QLineEdit):
	def __init__(self, parent):
		super(LineEditDialog, self).__init__()
		self.parentWindow = parent

	def keyPressEvent(self, event):
		None

