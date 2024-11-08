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


from datetime import datetime
from PySide6.QtCore import Qt, QDir
from PySide6.QtWidgets import QWidget, QFileDialog

from app.gui_design.ui_info import Ui_info


class CtmWidget(QWidget):
    def __init__(self, parent=None):
        QWidget.__init__(self, parent)

        self.ui = Ui_info()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.ui.btn_save.clicked.connect(self.save_logs)
        self.ui.info_screen.ensureCursorVisible()

    def hide_overlay(self):
        self.close()

    def save_logs(self):

        dir_to_use = QDir.homePath() + "/" + datetime.now().strftime("%Y%m%d_%H%M%S_logs.txt")
        log_path, _ = QFileDialog.getSaveFileName(self, caption="Save Logs",
                                                  dir=dir_to_use, filter='Text File (*.txt)')
        if log_path:
            with open(log_path, 'a+', ) as fid:
                fid.write(self.ui.info_screen.toPlainText())
