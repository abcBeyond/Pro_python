#! /usr/bin/python
# -*- coding:utf8 -*-

import sys
from PyQt4.QtCore import *
from PyQt4.QtGui import *
import ui_main

if __name__=="__main__":
	app=QApplication(sys.argv)
# 	##国际化部分
# 	#需要使用pylupdate4 *.py -ts ***.ts提取需要翻译的单词,然后通过linguist翻译发布qm文件	
	trans=QTranslator()
	trans.load("./serialPort_ch")
	app.installTranslator(trans)
# ##end 国际化	
	ui=ui_main.UIMain()	
	app.exec_()
