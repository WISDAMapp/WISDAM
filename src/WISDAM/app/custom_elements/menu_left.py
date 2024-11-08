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


from typing import Dict

from PySide6.QtCore import (QSize, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import QPushButton, QSizePolicy, QLayout

style_menu = """
                QPushButton {
                    background-image: INSERT_ICON_PATH;
                    background-position: left center;
                    background-repeat: no-repeat;
                    border: none;
                    border-left: 20px solid rgb(27, 29, 35);
                    background-color: rgb(27, 29, 35);
                    text-align: left;
                    padding-left: 45px;
                }
                QPushButton:pressed {
                    background-color: rgb(180, 150, 41);
                    border-left: 20px solid rgb(180, 150, 41);
                }
                """


class MenuButton(QPushButton):

    def __init__(self, name, icon):
        super().__init__()
        font = QFont()
        font.setFamily(u"Segoe UI")
        font.setPointSize(10)
        font.setBold(True)

        size_policy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.sizePolicy().hasHeightForWidth())
        self.setSizePolicy(size_policy)

        self.setMinimumSize(QSize(60, 60))
        self.setLayoutDirection(Qt.LeftToRight)
        self.setFont(font)
        self.setStyleSheet(style_menu.replace('INSERT_ICON_PATH', icon))
        self.setText(name)
        self.setToolTip(name)

    def set_active(self):
        # select = getStyle + ("QPushButton { border-right: 7px solid rgb(44, 49, 60); }")
        current_stylesheet = self.styleSheet()
        style_text = current_stylesheet.replace("background-color: rgb(27, 29, 35);",
                                                "background-color: rgb(180, 150, 41);")
        style_text = style_text.replace("border-left: 20px solid rgb(27, 29, 35);",
                                        "border-left: 20px solid rgb(180, 150, 41);")
        self.setStyleSheet(style_text)

    #  DESELECT
    def style_reset(self):
        current_stylesheet = self.styleSheet()
        style_text = current_stylesheet.replace("background-color: rgb(180, 150, 41);",
                                                "background-color: rgb(27, 29, 35);")
        style_text = style_text.replace("border-left: 20px solid rgb(180, 150, 41);",
                                        "border-left: 20px solid rgb(27, 29, 35);")
        self.setStyleSheet(style_text)


class MenuBar:

    def __init__(self, top_widget: QLayout, bottom_widget: QLayout, action):

        self.top_widget = top_widget
        self.bottom_widget = bottom_widget
        self.buttons: Dict[str, MenuButton] | None = {}
        self.current_name = ''
        self.action = action

    def add_button(self, name, icon, is_top_menu):

        btn = MenuButton(name, icon)
        btn.clicked.connect(lambda: self.action(name))
        self.buttons[name] = btn
        if is_top_menu:
            self.top_widget.addWidget(self.buttons[name])
        else:
            self.bottom_widget.addWidget(self.buttons[name])

    def set_active(self, name):

        if self.current_name:
            self.buttons[self.current_name].style_reset()
        self.current_name = name
        self.buttons[name].set_active()
