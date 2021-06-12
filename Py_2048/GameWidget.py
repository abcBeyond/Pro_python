# ！ -*- coding:utf-8 -*-

import random

from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import QParallelAnimationGroup, QPoint, QRect, QRectF, QPropertyAnimation, QEasingCurve
from PyQt5.QtGui import QColor, QPainter, QBrush, QPen, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget


class CPara:
    #
    space = 5

    #
    inter = 5

    #
    dir_up = 4
    dir_down = 3
    dir_left = 2
    dir_right = 1


class GameWidget(QWidget):
    """游戏元素"""
    signalGameOver = QtCore.pyqtSignal()
    value = []
    colors = [QColor.fromRgb(0xFF, 0xFF, 0xCC), QColor.fromRgb(0xFF, 0xFF, 0x99),
              QColor.fromRgb(0xFF, 0xCC, 0xCC), QColor.fromRgb(0xFF, 0xCC, 0x99),
              QColor.fromRgb(0xFF, 0x99, 0x99), QColor.fromRgb(0xFF, 0x99, 0x66),
              QColor.fromRgb(0xFF, 0x66, 0x66), QColor.fromRgb(0xCC, 0x99, 0x66),
              QColor.fromRgb(0xCC, 0x33, 0x33), QColor.fromRgb(0xCC, 0x00, 0x33),
              QColor.fromRgb(0xFF, 0x00, 0x00)]

    def __init__(self, width, num=5, parent=None):
        super(GameWidget, self).__init__(parent)
        self.rect_size = width
        self.space_size = 30
        self.rect_radius = 10
        self.num = num
        self.press_pos = None
        self.release_pos = None
        self.resize(self.rect_size, self.rect_size)
        self.start()

    def start(self):
        temp_value = []
        for i in range(self.num):
            for j in range(self.num):
                temp_value.append(0)
            self.value.append(temp_value)
            temp_value = []
        pos00 = random.randint(0, self.num - 1)
        pos01 = random.randint(0, self.num - 1)
        pos10 = random.randint(0, self.num - 1)
        pos11 = random.randint(0, self.num - 1)
        if QPoint(pos00, pos01) != QPoint(pos10, pos11):
            self.value[pos00][pos01] = 2
            self.value[pos10][pos11] = 2
        else:
            self.start()

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        brush = QBrush(QColor.fromRgb(141, 121, 81))
        painter.setBrush(brush)
        painter.drawRoundedRect(QRect(0, 0, self.rect_size, self.rect_size), self.rect_radius, self.rect_radius)

        rect_len = (self.rect_size - CPara.inter * (self.num + 1)) / self.num
        rect_e_space = CPara.inter
        painter.save()
        pen_ = QPen(Qt.white)
        pen_.setWidth(2)
        painter.setPen(pen_)

        font = QFont()
        font.setFamily("Courier")
        font.setBold(True)
        font.setPixelSize(self.width() / 15)

        for x in range(self.num):
            for y in range(self.num):
                _pen = QPen()
                _pen.setBrush(Qt.white)
                _pen.setWidth(3)
                painter.setPen(Qt.NoPen)
                painter.setBrush(self.get_color(self.value[y][x]))
                painter.drawRoundedRect(QRectF(0 + rect_e_space + (rect_e_space + rect_len) * x,
                                               0 + rect_e_space + (rect_e_space + rect_len) * y, rect_len, rect_len),
                                        self.rect_radius,
                                        self.rect_radius)
                painter.setPen(QPen(QColor(0, 0, 0)))
                painter.setFont(font)
                if self.value[y][x] != 0:
                    painter.drawText(
                        QRectF(0 + rect_e_space + (rect_e_space + rect_len) * x,
                               0 + rect_e_space + (rect_e_space + rect_len) * y, rect_len, rect_len), Qt.AlignCenter,
                        str(self.value[y][x]))
        painter.restore()

    def mousePressEvent(self, e):
        self.press_pos = e.pos()

    def mouseReleaseEvent(self, e):
        self.release_pos = e.pos()
        x = abs(self.release_pos.x() - self.press_pos.x())
        y = abs(self.release_pos.y() - self.press_pos.y())
        direct = 0
        if x > y:
            if self.release_pos.x() > self.press_pos.x():
                direct = CPara.dir_right  # right
            else:
                direct = CPara.dir_left  # left
        else:
            if self.release_pos.y() > self.press_pos.y():
                direct = CPara.dir_down  # down
            else:
                direct = CPara.dir_up  # up
        self.re_build_array(direct)

    def re_build_array(self, direct):
        if direct == CPara.dir_right or direct == CPara.dir_left:
            for i in range(self.num):
                self.value[i] = self.re_build_one_line(self.value[i], direct)
        elif direct == CPara.dir_down or direct == CPara.dir_up:
            for j in range(self.num):
                temp_row = []
                for m in range(self.num):
                    temp_row.append(self.value[m][j])
                temp_row_result = self.re_build_one_line(temp_row, direct)
                for n in range(self.num):
                    self.value[n][j] = temp_row_result[n]
        self.addNewPoint()
        self.update()

    def re_build_one_line(self, line_data, direct):
        temp = [0] * len(line_data)
        start_pos = 0
        if direct == CPara.dir_right or direct == CPara.dir_down:
            line_data = reversed(line_data)

        for data in line_data:
            if data == 0:
                continue
            else:
                temp[start_pos] = data
                start_pos = start_pos + 1

        for i in range(len(temp) - 1):
            if temp[i] == 0 and temp[i + 1] != 0:
                temp[i] = temp[i + 1]
                temp[i + 1] = 0
            if temp[i] == temp[i + 1]:
                temp[i] = temp[i] + temp[i]
                temp[i + 1] = 0
        if direct == CPara.dir_right or direct == CPara.dir_down:
            temp = self.rever_list(temp)
        return temp

    def rever_list(self, ll):
        temp = []
        for data in reversed(ll):
            temp.append(data)
        return temp

    def addNewPoint(self):
        flag = 0
        for i in range(self.num):
            for j in range(self.num):
                if self.value[i][j] == 0:
                    flag = 1
        if flag == 0:
            if self.check_game_over():
                print(self.tr("Game Over"))
                self.signalGameOver.emit()
            else:
                print(self.tr("Game on"))
        else:
            self.new_point()

    def new_point(self):
        pos00 = random.randint(0, self.num - 1)
        pos01 = random.randint(0, self.num - 1)
        if self.value[pos00][pos01] == 0:
            self.value[pos00][pos01] = 2
        else:
            self.new_point()

    def get_color(self, number):
        if number == 0:
            return self.colors[0]
        for i in range(100):
            if number == (int)(1 << i):
                return self.colors[i]
        return None

    def check_game_over(self):
        bret = False
        for i in range(self.num):
            for j in range(self.num):
                if self.check_point_has_some(i, j):
                    return bret
        return True

    def check_point_has_some(self, i, j):
        valet = self.value[i][j]
        iret = 1
        if j - 1 >= 0:
            up = self.value[i][j - 1]
            if up == valet:
                return iret
        if j + 1 < self.num:
            down = self.value[i][j + 1]
            if down == valet:
                return iret
        if i + 1 < self.num:
            right = self.value[i + 1][j]
            if right == valet:
                return iret
        if i - 1 >= 0:
            left = self.value[i - 1][j]
            if left == valet:
                return iret
        return 0

    def restart(self):
        self.value = []
        self.start()
        self.update()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        key_e = a0.key()
        _dir = None
        if key_e == Qt.Key_Up or key_e == Qt.Key_W:
            _dir = CPara.dir_up
        elif key_e == Qt.Key_Down or key_e == Qt.Key_S:
            _dir = CPara.dir_down
        elif key_e == Qt.Key_Left or key_e == Qt.Key_A:
            _dir = CPara.dir_left
        elif key_e == Qt.Key_Right or key_e == Qt.Key_D:
            _dir = CPara.dir_right
        else:
            return
        self.re_build_array(_dir)
