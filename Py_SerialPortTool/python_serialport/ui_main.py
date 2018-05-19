#! -*- coding:utf8 -*-

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4 import QtCore
import  ui_serialport
import pro_network
import diacmdButton
import commonData

#特质button
class testButton(QPushButton):
	def __init__(self,strData,parent=None):
		super(testButton,self).__init__(parent)
		self.setGeometry(0,0,self.width(),self.width())
		self.setText(strData)
		self.show()
#控件绑定
class LabelAndCheckBox(QWidget):
	def __init__(self,lableName,comboboxStr):
		super(LabelAndCheckBox,self).__init__()
		label=QLabel(lableName+":")	
		combobox=QComboBox()
		combobox.addItems(comboboxStr)
		label.setGeometry(0,0,50,30)
		combobox.setGeometry(55,0,100,30)
		label.setParent(self)
		combobox.setParent(self)
		self.resize(150,35)
#主要用来画边界
class BaseSerialUI(QWidget):
	def __init__(self):
		super(BaseSerialUI,self).__init__()
		self.setPalette(QPalette(Qt.white))
		self.setAutoFillBackground(True)
		self.setMinimumSize(200,300)
	#控制连接方式高亮
		self.colorBack = False
	def paintEvent(self,event):
		painter = QPainter(self)
		rect = self.rect()
		painter.setPen(Qt.blue)
		if self.colorBack:
			painter.setBrush(Qt.blue)
		else:
			pass
		painter.drawRect(rect)
class SendCmdUI(BaseSerialUI):
	def __init__(self):
	 	super(SendCmdUI,self).__init__()
	 	self.lineEditData=QLineEdit("HELLO WORLD")
		self.sendButton=QPushButton(self.tr("send"))
#网络相关设置
class NetworkConnectUI(BaseSerialUI):
	showDataUI = QtCore.pyqtSignal(QString)
	signalSendDataToServer = QtCore.pyqtSignal(QByteArray,bool)
	signalSendDataToShowBusInfo = QtCore.pyqtSignal(QStringList)
	def __init__(self):
		super(NetworkConnectUI,self).__init__()
		gridLayout = QGridLayout()
		label_IP=QLabel(self.tr("IP"))
		label_socket=QLabel(self.tr("Socket"))	
		self.lineEdit_IP = QLineEdit("192.168.1.108")	
		self.lineEdit_socket=QLineEdit("1234")
		gridLayout.addWidget(label_IP,0,0)
		gridLayout.addWidget(self.lineEdit_IP,0,1)
		gridLayout.addWidget(label_socket,1,0)
		gridLayout.addWidget(self.lineEdit_socket,1,1)
		self.buttonConnect = QPushButton(self.tr("connect"))
		gridLayout.addWidget(self.buttonConnect,2,0)
		self.buttonDisConnect = QPushButton(self.tr("Disconnect"))
		gridLayout.addWidget(self.buttonDisConnect,2,1)
		gridLayout.setRowStretch(0,1)
		gridLayout.setRowStretch(1,1)
		gridLayout.setRowStretch(2,1)
		gridLayout.setRowStretch(3,1) #占位用 
		self.setLayout(gridLayout)
		self.netWorkProcess = pro_network.tcpDataTrans()
		self.connect(self.buttonConnect,SIGNAL("clicked()"),self.connectServer)	
		self.connect(self.buttonDisConnect,SIGNAL("clicked()"),self.DisConnectServer)	
		self.netWorkProcess.signalSendDataToUI.connect(self.sendDataToUI)
		self.netWorkProcess.signalConnectSuccess.connect(self.connectServerSuccess)
		self.netWorkProcess.signalConnectError.connect(self.connectErrorLog)
		self.netWorkProcess.signalSendIbusInfo.connect(self.signalSendDataToShowBusInfo)
		self.signalSendDataToServer.connect(self.netWorkProcess.sendDataToServer)
	def connectErrorLog(self,logInfo):
		self.buttonDisConnect.setEnabled(False)
		self.buttonConnect.setEnabled(True)
		QMessageBox.warning(self,self.tr("NetWorkInfo"),logInfo)
		self.lineEdit_IP.setReadOnly(False)	
		self.lineEdit_socket.setReadOnly(False)
		if self.colorBack == True:
			self.colorBack=False
			self.update()
	def connectServerSuccess(self):
		self.buttonDisConnect.setEnabled(True)
		self.colorBack=True
		self.update()
	def connectServer(self):
		# print("going to connectserver")
		self.buttonConnect.setEnabled(False)
		self.netWorkProcess.connectServer(self.lineEdit_IP.text(),self.lineEdit_socket.text())
		self.lineEdit_IP.setReadOnly(True)	
		self.lineEdit_socket.setReadOnly(True)
	def DisConnectServer(self):
		self.buttonConnect.setEnabled(True)
		self.buttonDisConnect.setEnabled(False)
		self.colorBack=False
		self.update()
		self.netWorkProcess.disconnectServer()
	def sendDataToServer(self,data):
		pass;
	def sendDataToUI(self,data):
		self.showDataUI.emit(data)
class SerialSettingUI(BaseSerialUI):
	def __init__(self):
		super(SerialSettingUI,self).__init__()
		layout=QVBoxLayout()
#读取设备中的串口设备名称
		strList = QStringList()
		for i in os.listdir("/dev"):
			strt=QString(i)
			if strt.contains("tty"):
				strList.append(i)
		layout.addWidget(LabelAndCheckBox(self.tr("port"),strList))
		bauds=["110","300","600","1200","2400","4800","9600","14400","19200","38400","56000","57600","115200"]
		strList.clear()
		for i in bauds:
			strList.append(i)
		layout.addWidget(LabelAndCheckBox(self.tr("baud"),strList))
		databits=["8","7","6"]
		strList.clear()
		for i in databits:
			strList.append(i)
		layout.addWidget(LabelAndCheckBox(self.tr("DataBit"),strList))
		checkbits=[self.tr("None"),self.tr("JiCheck"),self.tr("ouCheck"),self.tr("Mark"),self.tr("SpaceCheck")]
		strList.clear()
		for i in checkbits:
			strList.append(i)
		layout.addWidget(LabelAndCheckBox(self.tr("CheckBit"),strList))
		stopBits=["1","1.5","2"]
		strList.clear()
		for i in stopBits:
			strList.append(i)
		layout.addWidget(LabelAndCheckBox(self.tr("StopBit"),strList))
		layout.addWidget(QPushButton(self.tr("Open")))
		layout.addStretch(3)
		for i in range(5):
			layout.setStretch(i,1)
			pass;
		self.setLayout(layout)
#主界面
class MainWidget(QWidget):
	def __init__(self):
		super(MainWidget,self).__init__()
		self.layout = QHBoxLayout()
		self.vboxlayout = QVBoxLayout()
	
		#串口设置
		self.ui1=SerialSettingUI()
		# self.vboxlayout.addWidget(ui1)
		#网口设置	
		self.ui2=NetworkConnectUI()
		self.ui2.showDataUI.connect(self.textEditShow)		
		# self.vboxlayout.addWidget(self.ui2k)
		self.stackedLayout = QStackedLayout()
		self.stackedLayout.addWidget(self.ui1)	
		self.stackedLayout.addWidget(self.ui2)	
		# self.vboxlayout.addLayout(stackedLayout)
		# self.staticCmd=QPushButton(self.tr("staticCMD"))
		self.tabBar = QTabBar()
		self.tabBar.addTab(self.tr("SerialPort"))
		self.tabBar.addTab(self.tr("NetWork"))
		self.vboxlayout.addWidget(self.tabBar)
		self.vboxlayout.addLayout(self.stackedLayout)
		# self.vboxlayout.addWidget(self.staticCmd)
		self.vboxlayout.addStretch()
		vboxlayout1 = QVBoxLayout()
		vboxlayout1.addWidget(QLabel(self.tr("REV DATA SETTING")))
		self.revcheckBox1 = QCheckBox(self.tr("save the data as the file ....."))
		self.revcheckBox2 = QCheckBox(self.tr("show the HEX Data"))
		self.revcheckBox3 = QCheckBox(self.tr("show the date"))
		self.revcheckBox4 = QCheckBox(self.tr("stop show the data"))	
		vboxlayout1.addWidget(self.revcheckBox1)
		vboxlayout1.addWidget(self.revcheckBox2)
		vboxlayout1.addWidget(self.revcheckBox3)
		vboxlayout1.addWidget(self.revcheckBox4)
		self.vboxlayout.addLayout(vboxlayout1)	
		self.vboxlayout.addStretch()
		vboxlayout2 = QVBoxLayout()
		vboxlayout2.addWidget(QLabel(self.tr("SND SETTING")))
		self.sndcheckBox1 = QCheckBox(self.tr("use the file ....."))
		self.sndcheckBox2 = QCheckBox(self.tr("add the check result"))
		self.sndcheckBox3 = QCheckBox(self.tr("use the HEX DATA "))
		self.sndcheckBox4 = QCheckBox(self.tr("loop snd"))	
		vboxlayout2.addWidget(self.sndcheckBox1)
		vboxlayout2.addWidget(self.sndcheckBox2)
		vboxlayout2.addWidget(self.sndcheckBox3)
		vboxlayout2.addWidget(self.sndcheckBox4)
		self.vboxlayout.addLayout(vboxlayout2)	
		self.buttonClear = QPushButton(self.tr("clear"))
		self.vboxlayout.addWidget(self.buttonClear)	
		# self.vboxlayout.addStretch()
		#addstretch 也算在里面,可以用addStretchFactor(Widget,NUm)
		self.vboxlayout.setStretch(0,1)
		self.vboxlayout.setStretch(1,4)
		self.vboxlayout.setStretch(2,1)
		self.vboxlayout.setStretch(3,1)
		self.vboxlayout.setStretch(4,3)
		self.vboxlayout.setStretch(5,1)
		self.vboxlayout.setStretch(6,3)
		self.vboxlayout.setStretch(7,1)
		# self.vboxlayout.setStretch(3,4)
		self.vboxlayout.addStretch(4)
		self.layout.addLayout(self.vboxlayout)
		widget1 = QWidget()
		widget1.resize(600,300)	
		self.textEdit = QTextEdit()
		self.textEdit.setReadOnly(True)
		layoutT = QVBoxLayout()
		layoutT.addWidget(self.textEdit)
		layoutT.setStretch(0,4)
		layoutTH=QHBoxLayout()
		self.lineEditData= QTextEdit("")
		layoutTH.addWidget(self.lineEditData)
		widget =QWidget()
		layoutTH.addWidget(widget)
		self.sendButton= testButton(self.tr("send"),widget)
		layoutTH.setStretch(0,10)
		layoutTH.setStretch(1,1)
		layoutT.addLayout(layoutTH)
		layoutT.setStretch(0,20)	
		layoutT.setStretch(1,1)
		widget1.setLayout(layoutT)
		self.layout.addWidget(widget1)
		self.layout.setStretch(0,1)
		self.layout.setStretch(1,5)
		self.layout.setSpacing(7)
		self.layout.setMargin(5)
		self.setLayout(self.layout)
		self.tabBar.currentChanged.connect(self.changeStackedLayout)
		self.connect(self.sendButton,SIGNAL("clicked()"),self.sendData)
		# self.staticCmd.clicked.connect(self.getStaticCmd)
		self.revcheckBox2.clicked.connect(self.refreshTextEditShow)
		self.sndcheckBox3.clicked.connect(self.refreshTextEditSnd)
		self.buttonClear.clicked.connect(self.clearTextEdit)
		self.ui2.signalSendDataToShowBusInfo.connect(self.showDeviceInfo)
	def clearTextEdit(self):
		self.textEdit.clear()
	def refreshTextEditSnd(self):
		data = self.lineEditData.toPlainText()
		dataByte=None
		if self.sndcheckBox3.checkState()==Qt.Checked:
			# print "current status is:checked"	
			dataByte = data.toLatin1().toHex()
		else:
			# print "current status is:unchecked"	
			dataByte =QByteArray.fromHex(data.toLatin1())
		self.lineEditData.clear()
		self.lineEditData.append(QString(dataByte))
	def refreshTextEditShow(self):
		data = self.textEdit.toPlainText()
		if self.revcheckBox2.checkState()==Qt.Checked:
			# print "current status is:checked"	
			dataByte = data.toLatin1().toHex()
		else:
			# print "current status is:unchecked"	
			dataByte =QByteArray.fromHex(data.toLatin1())
		self.textEdit.clear()
		self.textEdit.append(QString(dataByte))
	def textEditShow(self,data):
		# print data
		dataShow = None
		if self.revcheckBox2.checkState() == Qt.Checked:
			# print "cheecked"
			dataShow = QString(data.toLatin1().toHex())
		else:
			dataShow = data
		self.textEdit.append(dataShow)
	def getStaticCmd(self):
		dialog = diacmdButton.ButtonDialog(self)
		dialog.setWindowTitle(self.tr("command select"))
		dialog.singalSendClickNumToMain.connect(self.getClickCommandNum)
		dialog.show()
	def showDeviceInfo(self,strList):
		listShow = [self.tr("Core Version"),self.tr("modApp version"),self.tr("PSAM Card No")
		,self.tr("Local IP")]	
		argvShow={} 
		lenData = len(listShow)
		for i in range(lenData):
			argvShow[listShow[i].toLatin1().data()] = strList[i]
		dialog = diacmdButton.diaDeviceInfo(self,**argvShow)
		dialog.setWindowTitle(self.tr("BusInfo"))
		dialog.exec_()
	def getDeviceInfo(self):
		self.ui2.signalSendDataToServer.emit(QByteArray(1,chr(0x00)),True)

	def sendData(self):
		# print("get the textedit data")
		dataTemp = self.lineEditData.toPlainText()
		dataSnd = None	
		if self.sndcheckBox3.checkState() == Qt.Checked:
			dataSnd = QByteArray.fromHex(dataTemp.toLatin1())
		else:
			dataSnd  = dataTemp.toLatin1()
		self.ui2.signalSendDataToServer.emit(dataSnd,False)
	def changeStackedLayout(self,data):
		# print("current chaned and data is:",data)
		self.stackedLayout.setCurrentIndex(data)
	def getClickCommandNum(self,data,extraData):
		# print "MainUI get Click data is:" ,data
		cmdData = commonData.cStaticData()
		cmd =cmdData.cmdStaticData[data]
		#self.textEdit.append(QString("SND:")+data+"\n")
		extraDataShow = extraData.right(extraData.length()-1)
		self.textEdit.append(QString("\nSND: ")+data + extraDataShow.toHex())
		# print("cmd is:",cmd)
		self.ui2.signalSendDataToServer.emit(QByteArray(1,chr(cmd))+extraData,True)

# 主界面
class UIMain(QMainWindow):
	def __init__(self):
		super(UIMain,self).__init__()
		self.resize(600,400)
		self.setWindowTitle(self.tr("Connect Test"))
		self.mainWidget = MainWidget()
		self.addMenu()
#		gridLayout = QGridLayout()
		self.setCentralWidget(self.mainWidget)
		self.show()
	def addMenu(self):
		self.action1 = QAction(self.tr("iBusInfo"),self)
		self.action = QAction(self.tr("iBusTestCmd"),self)
		self.menuFile = self.menuBar().addMenu(self.tr("&iBusTest"))		
		self.menuFile.addAction(self.action1)
		self.menuFile.addAction(self.action)
		self.action.triggered.connect(self.mainWidget.getStaticCmd)
		self.action1.triggered.connect(self.mainWidget.getDeviceInfo)
