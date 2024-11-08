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


from PySide6.QtCore import Signal, Qt, SignalInstance
from PySide6.QtWidgets import QWidget

from app.gui_design.ui_user import Ui_popup_user


class POPUPUser(QWidget):

    got_user: SignalInstance = Signal(str)

    def __init__(self):
        QWidget.__init__(self)
        self.ui = Ui_popup_user()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.ui.save_user.clicked.connect(self.save_user)

    def save_user(self):
        if not self.ui.input_user.text().lower() == 'user':
            self.got_user.emit(self.ui.input_user.text().lower())
            self.close()
        else:
            self.ui.user_error.setText('Please enter User')
