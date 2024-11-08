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


import logging

from PySide6.QtWidgets import QWidget
from PySide6.QtGui import (QColor)

from PySide6 import QtCore
from PySide6.QtCore import Qt, Signal, Slot

from app.gui_design.ui_config import Ui_popup_config

logger = logging.getLogger(__name__)


class POPUPConfiguration(QWidget):
    config_send = Signal(object)

    def __init__(self, parent=None):
        QWidget.__init__(self, parent)
        self.ui = Ui_popup_config()
        self.ui.setupUi(self)
        self.dragPos = QtCore.QPointF()
        self.pick_color = None
        self.reproject_color = None

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.ui.btn_close.clicked.connect(self.send_values)
        self.ui.btn_save.clicked.connect(self.send_values)
        self.ui.btn_color_pick.colorChanged.connect(self.get_color)
        self.ui.btn_color_reprojection.colorChanged.connect(self.get_color)

        def move_window(event):
            if event.buttons() == Qt.MouseButton.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_top.mouseMoveEvent = move_window

    def set_color_widget(self, color_scheme):
        self.pick_color = color_scheme[0]
        self.reproject_color = color_scheme[1]
        self.ui.btn_color_pick.set_color(QColor(color_scheme[0]))
        self.ui.btn_color_reprojection.set_color(QColor(color_scheme[1]))

    # Slots
    @Slot(QColor)
    def get_color(self, color):
        if self.sender().objectName() == 'btn_color_pick':
            self.pick_color = color.name(QColor.HexArgb)
        else:
            self.reproject_color = color.name(QColor.HexArgb)

    # EVENTS

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    @QtCore.Slot()
    def send_values(self):

        self.config_send.emit({0: self.pick_color, 1: self.reproject_color})
        self.close()
