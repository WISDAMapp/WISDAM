# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2025 Martin Wieser.
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


from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QCursor


from app.gui_design.ui_confirm import Ui_popup_confirm

logger = logging.getLogger(__name__)


class POPUPConfirm(QDialog):  # Inheritance of the QDialog class
    def __init__(self, text_to_display):
        super().__init__()
        self.ui = Ui_popup_confirm()
        self.ui.setupUi(self)
        pos = QCursor.pos()

        # Need to test on dual screen
        try:
            if pos.y() > self.screen().availableSize().height() - 150:
                pos.setY(pos.y() - 150)

            if pos.x() > self.screen().availableSize().width() - 300:
                pos.setX(pos.x() - 300)

            self.move(pos)
        except:
            pass

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.lbl_confirm.setText(text_to_display)
