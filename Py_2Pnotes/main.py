#! -*- coding:utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from mainWindow import MyMainWindow

if __name__ == "__main__":
	import sys
	app = QApplication(sys.argv)
        myWindow = MyMainWindow()
        myWindow.show()
	sys.exit(app.exec_())
