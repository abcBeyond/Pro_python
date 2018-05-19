#! -*- coding : utf8 -*-

from PyQt4.QtCore import QObject

class  cStaticData(QObject):
	def __init__(self):
		super(cStaticData,self).__init__()
		self.cmdStaticData={self.tr("Start"):0x01,self.tr("GetRandomData"):0x02,\
			self.tr("SelectDir"):0x03,self.tr("ReadBinFile"):0x04,self.tr("GetBalance"):0x05,self.tr("ReadRecordFile"):0x06}
