#! -*- coding:utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import *
from GameWidget import GameWidget


class UiButton(QPushButton):
    def __init__(self, text="PushButton", canClicked=True):
        super(UiButton, self).__init__()
        self.ttext = text
        self.setCheckable(canClicked)
        self.setFixedHeight(40)
        self.setFixedWidth(self.width() / 4)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen(Qt.NoPen))
        brush = QBrush(QColor.fromRgb(0xFF, 0xFF, 0xCC))
        painter.setBrush(brush)
        painter.drawEllipse(QRect(0, 0, e.rect().width(), e.rect().height()))
        font = QFont()
        font.setFamily("Courier")
        font.setBold(True)
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(QPen(Qt.black))
        painter.drawText(e.rect(), Qt.AlignCenter, self.ttext)


class MainWidget(QWidget):
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)
        self.setFixedSize(480, 640)
        self.buildUI()
        self.connect(self.button, SIGNAL("clicked()"), self.gameWidget.restart)

    def buildUI(self):

        _palette = self.palette()
        _palette.setBrush(QPalette.Background, Qt.black)
        self.setPalette(_palette)

        hboxLayout = QHBoxLayout()
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30)
        self.labelScore = UiButton("Score", False)
        hboxLayout.addWidget(self.labelScore)
        self.labelHighScore = UiButton("HighScore", False)
        hboxLayout.addWidget(self.labelHighScore)
        vboxLayout = QVBoxLayout()
        vboxLayout.addLayout(hboxLayout)
        hboxLayout1 = QHBoxLayout()
        hboxLayout1.addStretch()
        self.button = UiButton(self.tr("Restart"))
        self.button.setFixedWidth(self.width() / 3)
        self.button.setFont(font)

        hboxLayout1.addWidget(self.button)
        hboxLayout1.addStretch()
        vboxLayout.addLayout(hboxLayout1)
        vboxLayout.addStretch()
        vboxLayout.setStretch(0, 1)
        vboxLayout.setStretch(1, 1)
        vboxLayout.setStretch(2, 0.5)

        self.gameWidget = GameWidget(4, self)
        self.gameWidget.setGeometry(2, 150, self.width(), self.height() - 100 - 20)
        self.setLayout(vboxLayout)
        self.connect(self.gameWidget, SIGNAL("signalGameOver()"), self.slotGameOver)

    def slotGameOver(self):
        print "slot game over"
        btn = QMessageBox.warning(self, "Game Over", "Resart??", QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.Yes:
            self.gameWidget.restart()
