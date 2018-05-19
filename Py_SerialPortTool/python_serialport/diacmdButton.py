#! -*- coding:utf8 -*-

from PyQt4.QtCore import * 
from PyQt4.QtGui import * 
from PyQt4 import QtCore
import commonData
class MyButton(QPushButton):
	signalSendClickNum=QtCore.pyqtSignal(QString)
	def __init__(self,btName):
		super(MyButton,self).__init__()
		self.setText(btName)
		self.clicked.connect(self.sndClickNum)
	def sndClickNum(self):
		self.signalSendClickNum.emit(self.text())
class readFileDialog(QDialog):
	signalSendRadioStatus=QtCore.pyqtSignal(QByteArray)
	def __init__(self,parent=None):
		super(readFileDialog,self).__init__()
		self.resize(300,200)
		layout = QVBoxLayout()
		# layout.addWidget(QRadioButton(self.tr("current dir")))
		# layout.addWidget(QCheckBox(self.tr("other dir")))
		buttonGroup = QButtonGroup(self)
		self.radio1 = QRadioButton(self.tr("Current RecordFile"))
		self.radio2 = QRadioButton(self.tr("Other RecordFile ......"))
		self.radio1.setChecked(True)
		buttonGroup.addButton(self.radio1,1)
		buttonGroup.addButton(self.radio2,2)
		layout.addWidget(self.radio1)
		layout.addWidget(self.radio2)
		layout.addStretch()
		self.lineEdit = QLineEdit("input RecordFile here")
		self.lineEdit.setEnabled(False)
		layout.addWidget(self.lineEdit)
		layout.addStretch()
		self.lineEditRecordID = QLineEdit(self.tr("input RecordNum here"))
		layout.addWidget(self.lineEditRecordID)
		layout.addStretch()
		buttonOK=QPushButton(self.tr("OK"))
		layout.addWidget(buttonOK)
		layout.addStretch()
		self.setLayout(layout)
		self.radio1.clicked.connect(self.radio1Exec)	
		self.radio2.clicked.connect(self.radio2Exec)
		buttonOK.clicked.connect(self.getStatus)
	def radio1Exec(self):
		if self.radio1.isChecked() == True:
			self.lineEdit.setEnabled(False) 
	def radio2Exec(self):
		if self.radio2.isChecked() == True:
			self.lineEdit.setEnabled(True) 
			self.lineEdit.setCursorPosition(0)
	def getStatus(self):
		if self.radio1.isChecked():
			datatemp = QByteArray.fromHex(self.lineEditRecordID.text().toLatin1())
			dataLen = chr(datatemp.size()&0x000000FF)
			sndData = QByteArray(1,chr(0x00))+QByteArray(1,dataLen)+datatemp
			self.signalSendRadioStatus.emit(sndData)
			self.close()
		elif self.radio2.isChecked():
			dataDirTemp = QByteArray.fromHex(self.lineEdit.text().toLatin1())
			dataDirLen = chr(dataDirTemp.size() & 0x000000FF)
			datatemp = QByteArray.fromHex(self.lineEditRecordID.text().toLatin1())
			dataLen = chr(datatemp.size()&0x000000FF)
			sndData = QByteArray(1,dataDirLen)+dataDirTemp+QByteArray(1,dataLen)+datatemp
			self.signalSendRadioStatus.emit(sndData)
			self.close()
		else:
			QMessageBox.waring(self,self.tr("Warning"),self.tr("you should select some case"))

class inputDialog(QDialog):
	signalSendInputDialog=QtCore.pyqtSignal(QByteArray)
	def __init__(self,name):
		super(inputDialog,self).__init__()
		self.resize(200,100)
		self.setWindowTitle(name)
		layout = QVBoxLayout()
		self.lineEdit = QLineEdit()
		layout.addWidget(self.lineEdit)
		layout.addStretch()
		buttonOK = QPushButton(self.tr("ok"))
		layout.addWidget(buttonOK)
		buttonOK.clicked.connect(self.clickOK)	
		self.setLayout(layout)
	def clickOK(self):
		datatemp = QByteArray.fromHex(self.lineEdit.text().toLatin1())
		dataLen=chr(datatemp.size() & 0xFF)
		sndData = QByteArray(1,dataLen)+datatemp
		self.signalSendInputDialog.emit(sndData)
		self.close()
class ButtonDialog(QDialog):
	'the command select UI'
	singalSendClickNumToMain=QtCore.pyqtSignal(QString,QByteArray)
	def __init__(self,parent):
		super(ButtonDialog,self).__init__(parent)
		self.buttons=[]	
		self.addButtons()	
		self.gridLyout=QGridLayout()
		self.columns = 4
		self.count = 0
		self.extraData = QByteArray()
		self.setMaximumSize(300,600)
		self.data = "ATS" 
		for i in self.buttons:
			self.gridLyout.addWidget(i,self.count/self.columns,self.count%self.columns)
			self.count = self.count + 1
		# self.buttonClick=QPushButton(self.tr("send"))
		# self.buttonClick.setMaximumWidth(100)
		self.buttonClickexit=QPushButton(self.tr("quit"))
		self.buttonClickexit.setMaximumWidth(100)
		hboxLayout = QHBoxLayout()
		hboxLayout.addStretch()
		# hboxLayout.addWidget(self.buttonClick)	
		# hboxLayout.addStretch()
		hboxLayout.addWidget(self.buttonClickexit)	
		hboxLayout.addStretch()
		self.hboxLayout = QVBoxLayout()
		self.hboxLayout.addStretch()
		self.hboxLayout.addLayout(self.gridLyout)
		self.hboxLayout.addStretch()
		self.hboxLayout.addLayout(hboxLayout)
		self.hboxLayout.addStretch()
		self.hboxLayout.setStretchFactor(self.gridLyout,3)
		self.hboxLayout.setStretchFactor(hboxLayout,1)

		self.setLayout(self.hboxLayout)	
		# self.buttonClick.clicked.connect(self.clickOkButton)
		self.buttonClickexit.clicked.connect(self.clickOkButtonexit)
		for i in self.buttons:
			i.signalSendClickNum.connect(self.getNum)
		self.show()
	def addButtons(self):
		data = commonData.cStaticData()
		for (k,v) in data.cmdStaticData.items():
			self.buttons.append(MyButton(k))

	def clickOkButtonexit(self):
		self.close()
	def readRecordCmd(self,extraData):
		# print("extraData is:",extraData.toHex())
		self.extraData = extraData
		self.singalSendClickNumToMain.emit(self.data,self.extraData)
	def getNum(self,data):
		self.extraData.clear()
		# print("get num is:%s" %(data))
		self.data = data	
		if data == self.tr("ReadRecordFile"):
			diaselect = readFileDialog(self)
			diaselect.signalSendRadioStatus.connect(self.readRecordCmd)
			diaselect.exec_()
		elif data == self.tr("ReadBinFile"):
			diaselect = inputDialog(self.tr("input the bin file"))
			diaselect.signalSendInputDialog.connect(self.readRecordCmd)
			diaselect.exec_()
		elif data == self.tr("SelectDir"):
			diaselect = inputDialog(self.tr("input the dir name"))
			diaselect.signalSendInputDialog.connect(self.readRecordCmd)
			diaselect.exec_()
		else:
			self.singalSendClickNumToMain.emit(self.data,QByteArray())
class treeTest(QWidget):
	def __init__(self):
		super(treeTest,self).__init__()
		treeWidget = QTreeWidget(self)
		# treeWidget.setColumnCount(1)
		strList = QStringList()
		strList<<"123"
		strList.append("234")
		treeItems=[]
		treeItems.append(QTreeWidgetItem(treeWidget,strList))
		treeItems.append(QTreeWidgetItem(treeWidget,QStringList("234")))
		treeWidget.addTopLevelItems(treeItems)
		self.show()
class labelAndLineEdit(QWidget):
	def __init__(self,str1,str2):
		super(labelAndLineEdit,self).__init__()
		self.setMaximumWidth(300)
		layout = QHBoxLayout()
		self.label = QLabel()
		self.label.setMinimumWidth(150)
		self.label.setText(str1+":")	
		self.lineEdit = QLineEdit()
		self.lineEdit.setText(str2)
		self.lineEdit.setReadOnly(True)
		layout.addWidget(self.label)
		# layout.addStretch()
		layout.addWidget(self.lineEdit)
		self.setLayout(layout)
class diaDeviceInfo(QDialog):
	def __init__(self,parent,**kargv):
		super(diaDeviceInfo,self).__init__(parent)
		self.setMaximumSize(400,400)
		layout = QVBoxLayout()
		for (label,edit) in kargv.items():
			layout.addWidget(labelAndLineEdit(label,edit))
		self.setLayout(layout)
