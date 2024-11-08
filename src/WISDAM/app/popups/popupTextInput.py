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


from PySide6.QtWidgets import QDialog
from PySide6.QtCore import Qt

from app.gui_design.ui_type import Ui_popup_type

logger = logging.getLogger(__name__)


class POPUPTextInput(QDialog):  # Inheritance of the QDialog class
    def __init__(self):
        super().__init__()
        self.ui = Ui_popup_type()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.btn_ok.clicked.connect(self.accept)
        self.ui.btn_cancel.clicked.connect(self.reject)
        self.ui.input_object_name.setFocus()

    def get_data(self):  # Defines the method of obtaining user input data
        return self.ui.input_object_name.text()
