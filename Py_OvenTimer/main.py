#! -*- coding:utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import math
class OvenTimerWidget(QWidget):
    MaxMinutes=45
    DegreesPerMinute=7.0
    MaxSeconds = MaxMinutes*60
    UpdateInterval = 5
    DegreesPerSecond=DegreesPerMinute/60
    def __init__(self,ovenSize = 1):
        super(OvenTimerWidget,self).__init__()
        self.setFixedSize(600,600)
        self.finishTime = QDateTime.currentDateTime()
        self.updateTimer = QTimer()
        self.connect(self.updateTimer,SIGNAL("timeout()"),self.update)

        self.finishTimer = QTimer()
        self.finishTimer.setSingleShot(True)
        # self.connect(self.finishTimer,SIGNAL("timeout()"),self.timeout)
        self.connect(self.finishTimer,SIGNAL("timeout()"),self.updateTimer.stop)

        font = QFont()
        font.setPointSize(28)
        self.setFont(font)

    def setDuration(self,secs):
        secs = max(0,min(secs,self.MaxSeconds))
        self.finishTime = QDateTime.currentDateTime().addSecs(secs) 
        if secs>0:
            self.updateTimer.start(self.UpdateInterval*1000)
            self.finishTimer.start(secs*1000)
        else:
            self.updateTimer.stop()
            self.finishTimer.stop()
        self.update()
    def paintEvent(self,e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing,True)
        side = min(self.width(),self.height())
        print "side is",side 
        painter.setViewport((self.width()-side)/2,(self.height()-side)/2,side,side)
        painter.setWindow(-50,-50,100,100)
        self.draw(painter)
    def draw(self,p):
        print self.palette().foreground()
        thickPen = QPen(self.palette().foreground(),1.5)
        thinPen = QPen(self.palette().foreground(),0.5)
        niceBlue = QColor(150,150,200)

        p.setPen(thinPen)
        p.setBrush(self.palette().foreground())
        points = []
        points.append(QPoint(-2,-49))
        points.append(QPoint(+2,-49))
        points.append(QPoint(0,-47))
        ploygon = QPolygon(points)
        p.drawPolygon(ploygon)

        coneGradient = QConicalGradient(0,0,-90.0)
        coneGradient.setColorAt(0.0,Qt.darkGray)
        coneGradient.setColorAt(0.2,niceBlue)
        coneGradient.setColorAt(0.5,Qt.white)
        coneGradient.setColorAt(1.0,Qt.darkGray)

        p.setBrush(coneGradient)
        p.drawEllipse(-46,-46,92,92)

        haloGradient = QRadialGradient(0,0,20,0,0)
        haloGradient.setColorAt(0.0,Qt.lightGray)
        haloGradient.setColorAt(0.8,Qt.darkGray)
        haloGradient.setColorAt(0.9,Qt.white)
        haloGradient.setColorAt(1.0,Qt.black)

        p.setPen(Qt.NoPen)
        p.setBrush(haloGradient)
        p.drawEllipse(-20,-20,40,40)

        knobGradient = QLinearGradient(-7,-25,7,-25)
        knobGradient.setColorAt(0.0,Qt.black)
        knobGradient.setColorAt(0.2,niceBlue)
        knobGradient.setColorAt(0.3,Qt.lightGray)
        knobGradient.setColorAt(0.8,Qt.white)
        knobGradient.setColorAt(1.0,Qt.black)

        p.rotate(self.duration()*self.DegreesPerSecond)
        p.setBrush(knobGradient)
        p.setPen(thinPen)
        p.drawRoundRect(-7,-25,14,50,99,49)
        p.rotate(-self.duration()*self.DegreesPerSecond)

        for i in xrange(self.MaxMinutes+1):
            if (i%5) == 0:
                p.setPen(thickPen)
                p.drawLine(0,-41,0,-44)
            else:
                p.setPen(thinPen)
                p.drawLine(0,-42,0,-44)
            p.rotate(-self.DegreesPerMinute)
    def duration(self):
        secs = QDateTime.currentDateTime().secsTo(self.finishTime)
        if secs < 0:
            secs = 0
        return secs
    def mousePressEvent(self,e):
        point = e.pos()-self.rect().center() 
        theta = math.atan2(-point.x(),-point.y())*180/math.pi 
        self.setDuration(self.duration()+int(theta/self.DegreesPerSecond))
        self.update()
import sys
app =QApplication(sys.argv)
otw = OvenTimerWidget()
otw.show()
sys.exit(app.exec_())
