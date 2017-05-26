import sys
from PyQt5.QtWidgets import (QLineEdit, QSlider, QPushButton, QVBoxLayout)
from PyQt5.QtWidgets import (QApplication, QWidget)
from PyQt5.QtCore import Qt

class MainWindow(QWidget):

	def __init__(self):
		super().__init__()
		self.initUI()

	def initUI(self):
		self.textField = QLineEdit()
		self.button1 = QPushButton("Clear")
		self.button2 = QPushButton("Print")
		self.slider = QSlider(Qt.Horizontal)
		self.slider.setMinimum(1)
		self.slider.setMaximum(99)
		self.slider.setValue(25)
		self.slider.setTickInterval(10)
		self.slider.setTickPosition(QSlider.TicksBelow)

		vBox = QVBoxLayout()
		vBox.addWidget(self.textField)
		vBox.addWidget(self.button1)
		vBox.addWidget(self.button2)
		vBox.addWidget(self.slider)

		self.setLayout(vBox)
		self.setWindowTitle("EPlusPlus")

		self.button1.clicked.connect(lambda: self.btnClick(self.button1, "Hello from Clear"))
		self.button2.clicked.connect(lambda: self.btnClick(self.button2, "Hello from Print"))
		self.slider.valueChanged.connect(self.vChange)

		self.show()

	def btnClick(self, b, string):
		if b.text() == "Print":
			print(self.textField.text())
		else:
			self.le.clear()

	def vChange(self):
		value = str(self.slider.value())
		self.le.setText(value)

app = QApplication(sys.argv)
window = MainWindow()
sys.exit(app.exec_())
