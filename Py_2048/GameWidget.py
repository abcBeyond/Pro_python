#！ -*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtOpenGL import QGLWidget
import random
import math
from PyQt4 import QtCore

class GameWidget(QGLWidget):
	signalGameOver=QtCore.pyqtSignal()
	value=[]
	colors=[QColor.fromRgb(0xFF, 0xFF, 0xCC), QColor.fromRgb(0xFF, 0xFF, 0x99),
    QColor.fromRgb(0xFF, 0xCC, 0xCC), QColor.fromRgb(0xFF, 0xCC, 0x99),
    QColor.fromRgb(0xFF, 0x99, 0x99), QColor.fromRgb(0xFF, 0x99, 0x66),
    QColor.fromRgb(0xFF, 0x66, 0x66), QColor.fromRgb(0xCC, 0x99, 0x66),
    QColor.fromRgb(0xCC, 0x33, 0x33), QColor.fromRgb(0xCC, 0x00, 0x33),
    QColor.fromRgb(0xFF, 0x00, 0x00)]	
	def __init__(self,num=5,parent=None):
		super(GameWidget,self).__init__(parent)
		tempValue=[]
		self.num=num
		self.start()	
		self.resize(400,400)
		print self.value
	def start(self):
		tempValue=[]
		for i in xrange(self.num):
			for j in xrange(self.num):
				tempValue.append(0)
			self.value.append(tempValue)
			tempValue=[]
		numtemp=len(self.colors)
		pos00=random.randint(0,self.num-1)	
		pos01=random.randint(0,self.num-1)
		pos10=random.randint(0,self.num-1)	
		pos11=random.randint(0,self.num-1)
		if QPoint(pos00,pos01) != QPoint(pos10,pos11):
			self.value[pos00][pos01]=2
			self.value[pos10][pos11]=2
		else:
			self.start()
	def paintEvent(self,e):
		painter = QPainter(self)
		painter.setRenderHint(QPainter.Antialiasing)
		brush = QBrush(QColor.fromRgb(141,121,81))
		painter.setBrush(brush)
		painter.setPen(Qt.NoPen)
		# painter.drawRect(0,0,100,100)
		painter.drawRoundedRect(QRect(0,0,self.width(),self.height()),30,30)
		font = QFont()
		font.setFamily("Consolas")
		font.setBold(True)
		font.setPixelSize(self.width()/10)
		painter.setFont(font)

		brush=QBrush(QColor.fromRgb(0xFF, 0xFF, 0xCC))
		pen = QPen()
		pen.setColor(QColor.fromRgb(141,121,81))
		pen.setWidth(self.width()/70)	
		painter.setBrush(brush)
		painter.setPen(pen)
		color=None
		for i in xrange(self.num):
			for j in xrange(self.num):
				painter.setBrush(self.getColor(self.value[j][i]))	
				painter.drawRoundRect(QRect(i*(self.width()/self.num),j*(self.height()/self.num),self.width()/self.num,self.height()/self.num),30,30)
				painter.setFont(font)
				painter.setPen(QColor(0,0,0))
				# painter.setPen(Qt.NoPen)
				if self.value[j][i] != 0:
					painter.drawText(QRectF(i*(self.width()/self.num),j*(self.height()/self.num),self.width()/self.num,self.height()/self.num),Qt.AlignCenter,QString("%1").arg(self.value[j][i]))
	def mousePressEvent(self,e):
		self.pressPos=e.pos()
	def mouseReleaseEvent(self,e):
		self.releasePos = e.pos()
		x=abs(self.releasePos.x()-self.pressPos.x())
		y=abs(self.releasePos.y()-self.pressPos.y())
		direct=0
		if x>y:
			if self.releasePos.x()	> self.pressPos.x():
				direct=1 #right
			else:
				direct=2 #left
		else:
			if self.releasePos.y() > self.pressPos.y():
				direct=3 #down
			else :
				direct=4 #up
		self.reBuildArray(direct)
	def reBuildArray(self,direct):
		temp=[]
		if direct == 1 or direct ==2:
			for i in xrange(self.num):
				self.value[i]=self.reBuildOneLine(self.value[i],direct)
		elif direct==3 or direct==4:
			for j in xrange(self.num):
				tempRow=[]
				for m in xrange(self.num):
					tempRow.append(self.value[m][j])
				tempRowReult=self.reBuildOneLine(tempRow,direct)
				for n in xrange(self.num):
					self.value[n][j]=tempRowReult[n]
		self.addNewPoint()
		self.update()	
	def reBuildOneLine(self,lineData,direct):
		temp=[0]*len(lineData)
		endPos = len(lineData)-1
		startPos = 0
		front=0
		if direct == 1 or direct == 3:
			lineData = reversed(lineData)
		for data in lineData:
			if data == 0:
				continue
			else:
				temp[startPos]=data
				startPos=startPos+1
		for i in xrange(len(temp)-1):
			if temp[i] == 0 and temp[i+1] != 0:
				temp[i]=temp[i+1]
				temp[i+1]=0
			if temp[i] == temp[i+1]:
				temp[i] = temp[i]+temp[i]
				temp[i+1]=0
		if direct==1 or direct == 3:
			temp=self.reverList(temp)
		return temp
	def reverList(self,ll):
		temp=[]
		for data in reversed(ll):
			temp.append(data)
		return temp
	def addNewPoint(self):
		flag=0
		for i in xrange(self.num):
			for j in xrange(self.num):
				if self.value[i][j] == 0:
					flag = 1
		if flag == 0:
			if self.checkGameOver():
				print "Game Over"
				self.signalGameOver.emit()
			else:
				print "Go on"
		else:
			self.newPoint()
	def newPoint(self):
			pos00=random.randint(0,self.num-1)	
			pos01=random.randint(0,self.num-1)
			if self.value[pos00][pos01] == 0:
				self.value[pos00][pos01] = 2
			else:
				self.newPoint()	
	def getColor(self,number):
		if number == 0:
			return self.colors[0]
		for i in range(100):
			if number == (int)(1<<i):
				return self.colors[i]
		return None
	def checkGameOver(self):
		bret=False
		for i in xrange(self.num):
			for j in xrange(self.num):
				if self.checkPointHasSome(i,j):
					return bret
		return True	
	def checkPointHasSome(self,i,j):
		valuet =self.value[i][j]
		iret = 1
		if j-1>=0:
			up=self.value[i][j-1]
			if up == valuet:
				return iret
		if j+1<self.num:
			down = self.value[i][j+1]
			if down == valuet:
				return iret
		if i+1<self.num:
			right = self.value[i+1][j]
			if right == valuet:
				return iret
		if i-1>=0:
			left = self.value[i-1][j]
			if left == valuet:
				return iret
		return 0
	def restart(self):
		self.value=[]
		self.start()
		self.update()
# if __name__=="__main__":
# 	import sys
# 	app = QApplication(sys.argv)	
# 	gw=GameWidget(4)
# 	gw.show()
# 	sys.exit(app.exec_())

