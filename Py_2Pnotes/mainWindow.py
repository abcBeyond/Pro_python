#! -*- coding:utf-8 -*-

from PyQt4.QtCore import *
from PyQt4.QtGui import *
import pyqrc
class MyMainWindow(QMainWindow):
	def __init__(self):
		super(MyMainWindow,self).__init__()
		self.setWindowTitle(self.tr("2PNotes"))
		self.setWindowIcon(QIcon(":/pic/icon/myLabel"))
		self.initui()
	def initui(self):
		self.mb = self.menuBar()
		font =QFont()
		font.setPixelSize(15)
		self.mb.setFont(font)
		#Menu File
		self.menuFile = self.mb.addMenu(self.tr("&File"))
		# self.menuFile.setFont(font)
		self.actionNew = QAction(QIcon(":/pic/icon/new"),self.tr("New"),self)
		self.actionOpen = QAction(QIcon(":/pic/icon/open"),self.tr("Open"),self)
		self.actionSave = QAction(QIcon(":/pic/icon/save"),self.tr("Save"),self)
		self.actionSaveAs = QAction(self.tr("Save As..."),self)
		self.actionPageSetUp = QAction(self.tr("Page Setup..."),self)
		self.actionPrintPreview = QAction(self.tr("Print Preview..."),self)
		self.actionPrint = QAction(QIcon(":/pic/icon/print"),self.tr("Print"),self)
		self.actionClose = QAction(QIcon(":/pic/icon/fileclose"),self.tr("Close"),self)
		self.actionExit = QAction(QIcon(":/pic/icon/exit"),self.tr("Exit"),self)

                self.actionNew.setToolTip(self.tr("new file")) #鼠标在action上显示提示,toolbar

		self.menuFile.addAction(self.actionNew)
		self.menuFile.addAction(self.actionOpen)
		self.menuFile.addAction(self.actionSave)
		self.menuFile.addAction(self.actionSaveAs)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionPageSetUp)
		self.menuFile.addAction(self.actionPrintPreview)
		self.menuFile.addAction(self.actionPrint)
		self.menuFile.addSeparator()
		self.menuFile.addAction(self.actionClose)
		self.menuFile.addAction(self.actionExit)
		self.connect(self.actionExit,SIGNAL("triggered()"),self.quitApp)

		#Menu Edit
		self.menuEdit =self.mb.addMenu(self.tr("&Edit"))
		self.actionNewEntry = QAction(QIcon(":/pic/icon/newRecord"),self.tr("New Entry"),self)
		self.actionDelEntry = QAction(QIcon(":/pic/icon/delRecord"),self.tr("Delete Entry"),self)
		self.actionCut = QAction(QIcon(":/pic/icon/cut"),self.tr("Cut"),self)
		self.actionCopy = QAction(QIcon(":/pic/icon/copy"),self.tr("Copy"),self)
		self.actionPaste = QAction(QIcon(":/pic/icon/paste"),self.tr("Paste"),self)
		self.actionChgKey = QAction(QIcon(":/pic/icon/key1"),self.tr("Change Key..."),self)

		self.menuEdit.addAction(self.actionNewEntry)
		self.menuEdit.addAction(self.actionDelEntry)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionCut)
		self.menuEdit.addAction(self.actionCopy)
		self.menuEdit.addAction(self.actionPaste)
		self.menuEdit.addSeparator()
		self.menuEdit.addAction(self.actionChgKey)


		#extra menu
		self.extraMenu = self.mb.addMenu(self.tr("&Extra"))
		self.actionFont = QAction(self.tr("Fonts"),self)
		self.actionEnableToolTips = QAction(self.tr("Enable ToolTips"),self)
		self.actionEnableToolTips.setCheckable(True)


		self.extraMenu.addAction(self.actionFont)
		self.extraMenu.addSeparator()
		self.extraMenu.addAction(self.actionEnableToolTips)

		self.aboutMenu = self.mb.addMenu(self.tr("&About"))

		self.actionAbout2Pnotes = QAction(QIcon(":/pic/icon/myLabel"),self.tr("About 2PNotes"),self)
		self.actionAboutQt = QAction(QIcon(":/pic/icon/qt-logo"),self.tr("QT"),self)
		self.aboutMenu.addAction(self.actionAbout2Pnotes)
		self.aboutMenu.addAction(self.actionAboutQt)

		self.connect(self.actionAboutQt,SIGNAL("triggered()"),self.myaboutQT)
		self.connect(self.actionAbout2Pnotes,SIGNAL("triggered()"),self.aboutThisApp)

		self.tbar = self.addToolBar("open")
		self.tbar.addAction(self.actionNew)
		self.tbar.addAction(self.actionOpen)
		self.tbar.addAction(self.actionSave)
		self.tbar.addSeparator()
		self.tbar.addAction(self.actionPrint)
		self.tbar.addAction(self.actionCut)
		self.tbar.addAction(self.actionCopy)
		self.tbar.addAction(self.actionPaste)
		self.tbar.addSeparator()
		self.tbar.addAction(self.actionNewEntry)
		self.tbar.addAction(self.actionDelEntry)
		self.tbar.addSeparator()
                self.tbar.addAction(self.actionExit)

                self.center = QWidget()
                self.labelBookMark =QLabel(self.tr("BookMark"))
                self.labelPasswd =QLabel(self.tr("Passwd"))
                self.editLineBookMark =QLineEdit()
                self.editLinePasswd =QLineEdit()
                self.textEdit = QTextEdit()
                self.labelAnnotations = QLabel(self.tr("Annotations"))
                self.textEdit2 = QTextEdit()
                layout = QGridLayout()
                layout.addWidget(self.labelBookMark,0,0)
                layout.addWidget(self.labelPasswd,0,1)
                layout.addWidget(self.editLineBookMark,1,0)
                layout.addWidget(self.editLinePasswd,1,1)
                layout.addWidget(self.textEdit,2,0)
                #layout.addWidget(self.labelAnnotations,2,1,1,1)
                vboxLayout = QVBoxLayout()
                vboxLayout.addWidget(self.labelAnnotations)
                vboxLayout.addWidget(self.textEdit2)
              #  vboxLayout.setStretch(0,1)
              #  vboxLayout.setStretch(1,)
                layout.addLayout(vboxLayout,2,1) 
                #layout.addWidget(self.textEdit2,3,1,1,4)

                self.center.setLayout(layout)
                self.setCentralWidget(self.center)
                self.resize(800,400)
	def quitApp(self):
		qApp.exit()
	def myaboutQT(self):
		qApp.aboutQt()
	def aboutThisApp(self):
		btn = QMessageBox.information(self,self.tr("About"),"Just Know that")

# import sys	
# app = QApplication(sys.argv)
# myWin=MyMainWindow()
# myWin.show()
# sys.exit(app.exec_())
