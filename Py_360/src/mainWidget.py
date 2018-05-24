#! -*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import sys
sys.path.append("../resource")
from source import *

class ShadowWidget(QWidget):
    def __init__(self,parent=None):
        super(ShadowWidget,self).__init__(parent)
        # 不显示最顶部的控制栏
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Dialog)
        self.isPressLeftMouse=False
        self.pressLeftMousePos=None
    def mousePressEvent(self,e):
        if e.button() == Qt.LeftButton:
            self.isPressLeftMouse = True
            self.pressLeftMousePos = e.pos()
    def mouseReleaseEvent(self,e):
        if e.button() == Qt.LeftButton:
            self.isPressLeftMouse = False
    def mouseMoveEvent(self,e):
        if self.isPressLeftMouse:
            self.move(e.globalPos()-self.pressLeftMousePos)
class MainWidget(ShadowWidget):
    def __init__(self,parent=None):
        super(MainWidget,self).__init__(parent)
        self.setFixedSize(900,600)
        self.setWindowIcon(QIcon(":/main/Logo"))

class BaseStyleWidget(QWidget):
    def __init__(self):
         super(BaseStyleWidget,self).__init__()
    def paintEvent(self,e):
        opt = QStyleOption()
        opt.init(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget,opt,painter,self)
if __name__=="__main__":
    app = QApplication(sys.argv)
    #mw = MainWidget()
    #mw.show()
    bsw = BaseStyleWidget()
    bsw.show()
    sys.exit(app.exec_())
