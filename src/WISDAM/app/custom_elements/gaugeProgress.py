# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2024 Martin Wieser.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see http://www.gnu.org/licenses/.
# ==============================================================================


from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QPainter, QPen, QPaintEvent, QFont, QStaticText, QFontMetrics


class GAUGEProgress(QWidget):
    """Custom Gauge to show some Statistics"""

    def __init__(self, parent=None):
        super(GAUGEProgress, self).__init__(parent)

        self.width = 150
        self.height = 150
        self.position_x = 0  # int(self.width / 2)
        self.position_y = 0  # int(self.height / 2)
        self.line_width = 30
        self.position_x_inner = int(self.position_x + self.line_width / 2)
        self.position_y_inner = int(self.position_y + self.line_width / 2)

        self.position_x_text = 0
        self.position_y_text = int(self.height * 0.66)

        self.color_progress = QColor(85, 170, 255)
        self.color_inner = QColor(58, 58, 107)
        self.color_outer = QColor(85, 85, 127, 100)

        self.text_font = 'Segoe UI'

        self.gauge_name_1 = ''
        self.gauge_name_2 = ''

        # Start of pie is at 3 o clock so to make zero on top it is +90 because its counterclockwise
        self._angle_start = 16 * 90
        self._angle = 0

        # font_static = QFont()
        # font_static.setFamily(self.text_font)
        # font_static.setPointSize(14)
        self.static_text = QStaticText()
        # self.static_text.prepare(font=font_static)
        self.static_text.setText(
            '<p align="center"><span style=" font-size:14px;font-weight:bold;">%s</span><br><span style=" '
            'font-size:14px;">%s</span></p>'
            % (self.gauge_name_1.upper(), self.gauge_name_2.upper()))

        self.position_x_static = int((self.width + self.line_width) / 2 - self.static_text.size().width() / 2)
        self.position_y_static = int((self.height + self.line_width) * 0.2)

        self.static_text_percent = QStaticText()
        font_static = QFont()
        font_static.setFamily(self.text_font)
        font_static.setPointSize(40)
        self.static_text_percent.setText('%')
        self.static_text.prepare(font=font_static)
        self.position_x_static_percent = 0
        self.position_y_static_percent = int((self.height + self.line_width) * 0.5)

        self.percent_text = '0'
        self.position_y_static_percent_text = int((self.height + self.line_width) * 0.8)
        self.position_x_static_percent_text = 0

    def set_initial(self, gauge_name_1: str, gauge_name_2: str,
                    color_progres: QColor,
                    color_inner: QColor,
                    color_outer: QColor):
        self.color_progress = color_progres
        self.color_inner = color_inner
        self.color_outer = color_outer

        self.gauge_name_1 = gauge_name_1
        self.gauge_name_2 = gauge_name_2

        self.static_text = QStaticText(
            '<p align="center"><span style=" font-size:14px;font-weight:bold;">%s</span><br><span style=" '
            'font-size:14px;">%s</span></p>'
            % (self.gauge_name_1.upper(), self.gauge_name_2.upper()))
        self.position_x_static = int((self.width + self.line_width) / 2 - self.static_text.size().width() / 2)
        self.position_y_static = int((self.height + self.line_width) * 0.2)

        self.change_value(0, 0)

    def change_value(self, count: int, max_count: int):

        if max_count < 1:
            self._angle = 0
            percent = 0
        else:
            self._angle = -int(count / max_count * 360 * 16)
            percent = (count / max_count * 100)

        self.percent_text = str(int(percent))

        font_percent = QFont()
        font_percent.setFamily(self.text_font)
        font_percent.setBold(True)
        font_percent.setPointSize(50)
        fm = QFontMetrics(font_percent)

        self.position_x_static_percent_text = int(
            (self.width + self.line_width) / 2 - fm.horizontalAdvance(self.percent_text) / 2)
        self.position_x_static_percent = int(
            (self.width + self.line_width) / 2 + fm.horizontalAdvance(self.percent_text) / 2)

        self.repaint()

    def paintEvent(self, event: QPaintEvent):
        paint_circle_background = QPainter(self)
        paint_circle_background.setRenderHint(QPainter.Antialiasing)
        paint_circle_background.setPen(QPen(Qt.PenStyle.NoPen))
        paint_circle_background.setBrush(self.color_outer)
        paint_circle_background.drawEllipse(self.position_x, self.position_y, self.width + self.line_width,
                                            self.height + self.line_width)

        paint_percent = QPainter(self)
        paint_percent.setRenderHint(QPainter.Antialiasing)
        paint_percent.setPen(QPen(Qt.PenStyle.NoPen))
        paint_percent.setBrush(self.color_progress)
        paint_percent.drawPie(self.position_x, self.position_y, self.width + self.line_width,
                              self.height + self.line_width, self._angle_start, self._angle)

        paint_circle = QPainter(self)
        paint_circle.setRenderHint(QPainter.Antialiasing)
        paint_circle.setPen(QPen(Qt.PenStyle.NoPen))
        paint_circle.setBrush(self.color_inner)
        paint_circle.drawEllipse(self.position_x_inner, self.position_y_inner, self.width, self.height)

        paint_text_static = QPainter(self)
        pen_text_static = QPen()
        pen_text_static.setColor(QColor(180, 180, 180))
        paint_text_static.setPen(pen_text_static)
        font_static = QFont()
        font_static.setFamily(self.text_font)
        # font_static.setPointSize(14)
        # font_static.setBold(True)
        paint_text_static.setFont(font_static)
        paint_text_static.drawStaticText(self.position_x_static, self.position_y_static, self.static_text)
        paint_text_static.end()

        paint_text = QPainter(self)
        pen_text = QPen()
        pen_text.setColor(self.color_progress)
        paint_text.setPen(pen_text)
        # font_percent = QFont()
        # font_percent.setFamily(self.text_font)
        # font_percent.setBold(True)
        # font_static.setPointSize(50)
        # paint_text.setFont(font_percent)
        paint_text.drawStaticText(self.position_x_static_percent, self.position_y_static_percent,
                                  self.static_text_percent)
        paint_text.end()

        paint_text = QPainter(self)
        pen_text = QPen()
        pen_text.setColor(self.color_progress)
        paint_text.setPen(pen_text)
        font_percent = QFont()
        font_percent.setFamily(self.text_font)
        font_percent.setBold(True)
        font_percent.setPointSize(50)
        paint_text.setFont(font_percent)
        paint_text.drawText(self.position_x_static_percent_text, self.position_y_static_percent_text,
                            self.percent_text)
        paint_text.end()
