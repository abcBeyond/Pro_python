#! -*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from GameWidget import GameWidget
class MainWidget(QWidget):
	def __init__(self,parent=None):
		super(MainWidget,self).__init__(parent)
		self.resize(408,606)
		self.buildUI()
		self.connect(self.button,SIGNAL("clicked()"),self.gameWidget.restart)
	def buildUI(self):
		hboxLayout=QHBoxLayout()
		font = QFont()
		font.setBold(True)
		self.labelScore=QLabel("Score")
		self.labelScore.setFont(font)
		hboxLayout.addWidget(self.labelScore)
		self.labelHighScore = QLabel()
		self.labelHighScore.setText("HighScore:")
		hboxLayout.addWidget(self.labelHighScore)
		vboxLayout = QVBoxLayout()
		vboxLayout.addLayout(hboxLayout)
		self.button = QPushButton(self.tr("&Restart"))
		self.button.setFixedWidth(self.width()/5)
		self.button.setFont(font)
		vboxLayout.addWidget(self.button,Qt.AlignCenter)
		vboxLayout.addSpacing(1)
		self.gameWidget = GameWidget()
		vboxLayout.addWidget(self.gameWidget)	
		vboxLayout.setStretch(0,1)
		vboxLayout.setStretch(1,1)
		vboxLayout.setStretch(2,1)
		vboxLayout.setStretch(3,5)
		self.setLayout(vboxLayout)
# if __name__=="__main__":
# 	import sys
# 	app = QApplication(sys.argv)
# 	gw = MainWidget()
# 	sys.exit(app.exec_())