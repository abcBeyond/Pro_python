#! -*- coding:utf-8 -*-
from PyQt5 import QtGui, QtCore
from PyQt5.QtCore import QRect, Qt, QPropertyAnimation, QByteArray
from PyQt5.QtGui import QPainter, QPen, QBrush, QColor, QFont, QPalette
from PyQt5.QtWidgets import QPushButton, QWidget, QMessageBox, QHBoxLayout, QVBoxLayout, QSizePolicy
from . import GameWidget


class UiButton(QPushButton):
    def __init__(self, text="PushButton", canclicked=True):
        super(UiButton, self).__init__()
        self.text = text
        self.setCheckable(canclicked)
        self.setFixedHeight(40)
        self.setFixedWidth(self.width() / 4)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setPen(QPen())
        brush = QBrush(QColor.fromRgb(0xFF, 0xFF, 0xCC))
        painter.setBrush(brush)
        painter.drawRect(QRect(0, 0, e.rect().width(), e.rect().height()))
        font = QFont()
        font.setFamily("Courier")
        font.setBold(True)
        font.setPixelSize(20)
        painter.setFont(font)
        painter.setPen(QPen(Qt.black))
        painter.drawText(e.rect(), Qt.AlignCenter, self.text)


class MainWidget(QWidget):
    def __init__(self, parent=None, config=None):
        super(MainWidget, self).__init__(parent)
        self.setWindowTitle(self.tr("G2048"))
        self.config = config.get()
        self.setFixedSize(self.config["size"]["width"], self.config["size"]["height"])
        self.build_ui()
        self.button.clicked.connect(self.gameWidget.restart)

    def build_ui(self):
        # 设置整体属性
        _palette = self.palette()
        self.setPalette(_palette)

        hbox_layout = QHBoxLayout()
        font = QFont()
        font.setBold(True)
        font.setPixelSize(30)
        # self.labelScore = UiButton(self.tr("Score"), False)
        # hbox_layout.addWidget(self.labelScore)
        # self.labelHighScore = UiButton(self.tr("HighScore"), False)
        # hbox_layout.addWidget(self.labelHighScore)
        vboxLayout = QVBoxLayout()
        hboxLayout1 = QHBoxLayout()
        # hboxLayout1.addStretch()
        self.button = UiButton(self.tr("Restart"))
        self.button.setFixedWidth(self.width() / 3)
        self.button.setFont(font)

        hboxLayout1.addWidget(self.button)
        vboxLayout.addLayout(hboxLayout1)
        hboxLayout1.addStretch()
        vboxLayout.addLayout(hbox_layout)
        vboxLayout.addStretch()
        vboxLayout.setStretch(0, 1)
        vboxLayout.setStretch(1, 1)
        vboxLayout.setStretch(2, 0.5)

        space_pos = GameWidget.CPara.space
        self.gameWidget = GameWidget.GameWidget(self.width() - 2 * space_pos, self.config["game"]["num"], self)
        self.gameWidget.setGeometry(space_pos, 150, self.width(), self.height() - 100 - 20)
        self.setLayout(vboxLayout)
        self.gameWidget.signalGameOver.connect(self.slot_gameover)

    def cal_game_widget_width(self):
        pass

    def slot_gameover(self):
        btn = QMessageBox.warning(self, self.tr("Game Over"), self.tr("Resart??"), QMessageBox.Yes | QMessageBox.No)
        if btn == QMessageBox.Yes:
            self.gameWidget.restart()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        self.gameWidget.keyPressEvent(a0)
