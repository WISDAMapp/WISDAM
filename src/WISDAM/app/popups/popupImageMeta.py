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

from app.gui_design.ui_image_meta import Ui_popup_image_meta

logger = logging.getLogger(__name__)


class POPUPImageMeta(QDialog):  # Inheritance of the QDialog class
    def __init__(self):
        super().__init__()
        self.ui = Ui_popup_image_meta()
        self.ui.setupUi(self)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.ui.btn_save.clicked.connect(self.accept)
        self.ui.btn_close.clicked.connect(self.reject)
        self.ui.txt_fligt_ref.setFocus()

    def set_data(self, flight_ref, transect, block, meta_user):
        # Set data

        self.ui.txt_fligt_ref.setText(flight_ref)
        self.ui.txt_transect.setText(transect)
        self.ui.txt_surveyblock.setText(block)

        self.ui.txt_operator.setText(meta_user['operator'])
        self.ui.txt_camera.setText(meta_user['camera_ref'])
        self.ui.txt_conditions.setText(meta_user['conditions'])
        self.ui.txt_comment.setPlainText(meta_user['comments'])

    def get_data(self):
        # Get user input data

        flight_ref = self.ui.txt_fligt_ref.text()
        transect = self.ui.txt_transect.text()
        block = self.ui.txt_surveyblock.text()

        operator = self.ui.txt_operator.text()
        camera_ref = self.ui.txt_camera.text()
        conditions = self.ui.txt_conditions.text()
        comments = self.ui.txt_comment.toPlainText()

        meta_user = {}
        if operator or camera_ref or conditions or comments:
            meta_user = {'operator': operator, 'camera_ref': camera_ref, 'conditions': conditions,
                         'comments': comments}

        return flight_ref, transect, block, meta_user
