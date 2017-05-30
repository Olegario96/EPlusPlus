from PyQt5.QtWidgets import QLineEdit, QFileDialog

##
## @brief      This class is a specialization of the class "QLineEdit". We use
##             the specialization to override the method "keyPressEvent". This
##             allow to every time that the user tries to type at the LineEdit
##             nothing will happen.
##
class LineEditDialog(QLineEdit):
	def __init__(self, parent):
		super(LineEditDialog, self).__init__()
		self.parentWindow = parent


	##
	## @brief      This method is a override. Every time the user tries to type
	##             something at the line Edit, nothing will happen.
	##
	## @param      self   Non static mehtod
	## @param      event  Event received from the Keyboard
	##
	## @return     This is a void function
	##
	def keyPressEvent(self, event):
		None

