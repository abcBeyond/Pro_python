#! coding:utf-8-*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
from MainWidget import MainWidget
if __name__=="__main__":
	app = QApplication(sys.argv)
	mw = MainWidget()
	mw.show()
	sys.exit(app.exec_())	
