#! -*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *

def moveToCenter(app,widget):
    deskWidth = app.desktop().width()
    deskHeight = app.desktop().height()
    appWidth = widget.width()
    appHeight = widget.height()
    widget.move((deskWidth-appWidth)/2,(deskHeight-appHeight)/2)
if __name__=="__main__":
    import sys
    app = QApplication(sys.argv)
#    widget = QWidget()
#    widget.resize(400,500)
#    moveToCenter(app,widget)
#    widget.show()
    sys.exit(app.exec_())

