import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox, QCheckBox, QLabel

##
## @brief      Class for dialog with check box. Since the PyQt5 implementation
##             doesn't have a dialog window with a check box, this is my
##             personal implementation. It just creates the text and adds the 
##             checkbox in the layout. The sys import is necessary for the 
##             args and kwargs.
##
class DialogWithCheckBox(QMessageBox):
	def __init__(self, parent=None):
		super(DialogWithCheckBox, self).__init__()
		msg = "                                                            "
		msg += "ATENÇÃO! \nPara que o programa funcione corretamente, não deve" 
		msg += " haver espaços em branco tanto no nome de pastas quanto dos" 
		msg += " arquivos. Para mais informação, por favor, leia o manual do usuário."

		self.setIcon(QMessageBox.Warning)
		self.setWindowTitle("EPlusPlus-WAR")
		self.setText(msg)

		self.checkBox = QCheckBox()
		self.checkBox.setText("Não avisar novamente")

		layout = self.layout()
		layout.addWidget(self.checkBox, 1, 2)

	##
	## @brief      Overrides the 'exec_' method from the 'QMessageBox' to return
	##             a tuple where the second element is the state of the check
	##             box. 
	##
	## @param      self    Non static metho
	## @param      args    The arguments
	## @param      kwargs  The kwargs
	##
	## @return     Returns a tuple where the second element is True if the check
	##             box is marked. False, otherwise.
	##
	def exec_(self, *args, **kwargs):
		return (QMessageBox.exec_(self, *args, **kwargs), self.checkBox.isChecked())