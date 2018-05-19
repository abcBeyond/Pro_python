# -*- coding:utf8 -*-

from PyQt4.QtCore import *

def printByteArray(data):
	print data.toHex()
class DataTrans:
	def __init__(self):
		self.headData = [0x3a]	
		self.tailData = [0x0d,0x0a]
	def formCmd(self,data):
		dataT = QByteArray()
		for i in self.headData:
			dataT.append(chr(i))
		dataT.append(chr(0x00))
		dataT.append(chr(data.size()))
		dataT.append(data)
		for i in self.tailData:
			dataT.append(chr(i))
		return dataT
	def anlyzeData(self,data):
		pass;
