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


from PySide6.QtCore import (Qt, Signal)
from PySide6.QtGui import (QMouseEvent)
from PySide6.QtWidgets import (QComboBox, QMenu)

from app.popups.popupTextInput import POPUPTextInput


class InteractiveCombo(QComboBox):
    """Combo with right click add or remove elements
    Two signals can be connected and used if elements added or deleted from combo"""

    # Signals which can be used to communicate an event happend
    add_signal = Signal(str)
    delete_signal = Signal(str)

    def __init__(self, parent):
        super(InteractiveCombo, self).__init__(parent)

        self.context_menu = QMenu()
        self.context_menu = QMenu()

        text = "Add Value"
        add_value = self.context_menu.addAction(text)
        add_value.triggered.connect(self.add_new_item)

        text = "Remove Value"
        remove = self.context_menu.addAction(text)
        remove.triggered.connect(lambda: self.delete_item(self.currentIndex()))

    def add_new_item(self):

        v = POPUPTextInput()
        if v.exec():
            name = v.get_data()

            if name:
                if not name.isspace():
                    if self.findText(name, flags=Qt.MatchFixedString) < 0:

                        self.insertItem(self.count() + 1, name)
                        self.add_signal.emit(name)

        self.setCurrentIndex(self.count() - 1)

    def delete_item(self, combo_index: int):

        item_text = self.itemText(combo_index)
        self.removeItem(combo_index)
        self.delete_signal.emit(item_text)

    def mousePressEvent(self, event: QMouseEvent) -> None:

        if event.button() == Qt.RightButton:
            global_pos = event.screenPos()
            self.context_menu.popup(global_pos.toPoint())

            return
        super(InteractiveCombo, self).mousePressEvent(event)
