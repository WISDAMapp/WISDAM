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


from PySide6.QtCore import (Signal, Qt)
from PySide6.QtGui import (QFont)
from PySide6.QtWidgets import (QComboBox, QLabel, QVBoxLayout, QWidget, QGridLayout, QSizePolicy)

from app.var_classes import ColorGui


class _ComboItem(QWidget):
    value_change = Signal()

    def __init__(self, parent, name, values, *args, **kwargs):
        super(_ComboItem, self).__init__(parent, *args, **kwargs)

        layout = QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(2)
        self.setFixedSize(120, 44)

        self.name = name

        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(True)
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setPointSize(12)

        self.label_name = QLabel()
        self.label_name.setFont(font)
        self.label_name.setText(name)
        self.label_name.setAlignment(Qt.AlignCenter)
        self.label_name.setFixedSize(120, 13)
        self.label_name.setStyleSheet("background-color: transparent")

        self.label_name.setSizePolicy(QSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed))

        self.combo = QComboBox()
        self.combo.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.combo.setFont(font2)
        self.combo.setStyleSheet(u"background-color: black;QComboBox { background-color: black;color: white;}\n"
                                 "QComboBox QAbstractItemView {\n"
                                 "  color: white\n"
                                 "}")
        self.combo.setEditable(False)
        self.combo.activated.connect(lambda: self.value_change.emit())

        self.combo.addItems(values)

        layout.addWidget(self.label_name)
        layout.addWidget(self.combo)
        self.setLayout(layout)

        p = self.sizePolicy()
        p.setRetainSizeWhenHidden(True)
        self.setSizePolicy(p)

    @property
    def value(self):
        return self.combo.currentText()

    @value.setter
    def value(self, value):
        self.combo.setCurrentText(value)

    def set_first(self):
        self.combo.setCurrentIndex(0)

    def set_data(self, name, values):
        self.label_name.setText(name)
        self.name = name
        self.combo.clear()
        self.combo.addItems(values)


class EnvironmentLayout(QWidget):
    """
    Custom Qt Widget for environment data. Up to 6 _ComboItem can be configurable be used
    """
    value_changed = Signal(object)

    def __init__(self, parent, *args, **kwargs):
        super(EnvironmentLayout, self).__init__(parent=parent, *args, **kwargs)
        self.data_env_items: list[_ComboItem] = []

        self.setAttribute(Qt.WA_StyledBackground, True)

        layout = QGridLayout()
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(6)

        self.data_env_items: list[_ComboItem] = []

        row = 0
        for idx in range(6):
            new_env_item = _ComboItem(self, ' ', [''])
            new_env_item.value_change.connect(self.value_send)
            new_env_item.hide()
            self.data_env_items.append(new_env_item)

            if idx > 2:
                row = 1
            col = idx - row * 3
            layout.addWidget(new_env_item, row, col, 1, 1)

        self.setLayout(layout)
        self.setStyleSheet("background-color: transparent")

    def set_config(self, config: None | dict):

        for item in self.data_env_items:
            self.setStyleSheet(ColorGui.color_env_none)
            item.set_data('', [])
            item.hide()

        if config is None:
            return

        for idx, (name, values) in enumerate(config.items()):
            self.data_env_items[idx].set_data(name, values)
            self.data_env_items[idx].show()

    def value_send(self):
        self.value_changed.emit(self.data)
        self.setStyleSheet(ColorGui.color_env_db)

    @property
    def data(self):

        data_collect = {'propagation': 0, 'data': {}}

        for item in self.data_env_items:
            if item.value:
                data_collect['data'][item.name] = item.value

        return data_collect

    @data.setter
    def data(self, dict_data):

        # This will show the first entry of the combos if
        # environment data is none
        if dict_data is None:
            self.setStyleSheet(ColorGui.color_env_none)
            for item in self.data_env_items:
                item.set_first()

        # set the values stored at the combo items
        else:
            if dict_data['propagation'] == 1:
                self.setStyleSheet(ColorGui.color_env_propagate)
            elif dict_data['propagation'] == 2:
                self.setStyleSheet(ColorGui.color_env_object)
            elif dict_data['propagation'] == 3:
                self.setStyleSheet(ColorGui.color_env_object_propagate)
            else:
                self.setStyleSheet(ColorGui.color_env_db)
            for name, value in dict_data['data'].items():

                for item in self.data_env_items:
                    if name == item.name:
                        item.value = value
                        break
