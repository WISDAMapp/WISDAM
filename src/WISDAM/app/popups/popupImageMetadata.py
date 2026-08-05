# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2026 Martin Wieser.
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


from __future__ import annotations

import json
from collections.abc import Mapping
from typing import Any

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QDialog,
    QHeaderView,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
)


class POPUPImageMetadata(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Metadata")
        self.resize(700, 500)
        self.setStyleSheet(
            """
            QDialog {
                background-color: rgb(34, 36, 50);
                color: rgb(210, 210, 210);
            }
            QTableWidget {
                background-color: rgb(27, 29, 35);
                alternate-background-color: rgb(38, 40, 56);
                color: rgb(210, 210, 210);
                gridline-color: rgb(52, 59, 72);
                border: 1px solid rgb(52, 59, 72);
                selection-background-color: rgb(85, 85, 127);
                selection-color: white;
            }
            QHeaderView::section {
                background-color: rgb(40, 44, 52);
                color: white;
                border: none;
                border-right: 1px solid rgb(52, 59, 72);
                border-bottom: 1px solid rgb(52, 59, 72);
                padding: 5px;
                font-weight: bold;
            }
            QPushButton {
                color: rgb(210, 210, 210);
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                background-color: rgb(52, 59, 72);
                padding: 6px 18px;
            }
            QPushButton:hover {
                background-color: rgb(57, 65, 80);
                border: 2px solid rgb(61, 70, 86);
            }
            QPushButton:pressed {
                background-color: rgb(35, 40, 49);
                border: 2px solid rgb(43, 50, 61);
            }
            QScrollBar:vertical {
                background: rgb(27, 29, 35);
                width: 14px;
                margin: 14px 0 14px 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(52, 59, 72);
                min-height: 25px;
                border-radius: 7px;
            }
            QScrollBar::handle:vertical:hover {
                background: rgb(57, 65, 80);
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: transparent;
                height: 14px;
            }
            QScrollBar:horizontal {
                background: rgb(27, 29, 35);
                height: 14px;
                margin: 0 14px 0 14px;
            }
            QScrollBar::handle:horizontal {
                background: rgb(52, 59, 72);
                min-width: 25px;
                border-radius: 7px;
            }
            QScrollBar::handle:horizontal:hover {
                background: rgb(57, 65, 80);
            }
            QScrollBar::add-line:horizontal,
            QScrollBar::sub-line:horizontal {
                background: transparent;
                width: 14px;
            }
            """
        )

        layout = QVBoxLayout(self)

        self.table = QTableWidget(self)
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Tag", "Value"])
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setWordWrap(False)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(
            0, QHeaderView.ResizeMode.ResizeToContents
        )
        self.table.horizontalHeader().setSectionResizeMode(
            1, QHeaderView.ResizeMode.Stretch
        )
        layout.addWidget(self.table)

        close_button = QPushButton("Close", self)
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button, alignment=Qt.AlignmentFlag.AlignRight)

    def set_metadata(self, metadata: Mapping[str, Any] | str | None) -> None:
        metadata_dict = self._metadata_dict(metadata)
        rows = list(metadata_dict.items()) if metadata_dict else [("metadata", "{}")]

        self.table.setRowCount(len(rows))
        item_flags = Qt.ItemFlag.ItemIsEnabled | Qt.ItemFlag.ItemIsSelectable
        for row, (key, value) in enumerate(rows):
            key_item = QTableWidgetItem(str(key))
            value_item = QTableWidgetItem(self._table_value(value))
            key_item.setFlags(item_flags)
            value_item.setFlags(item_flags)
            self.table.setItem(row, 0, key_item)
            self.table.setItem(row, 1, value_item)

        self.table.resizeRowsToContents()

    @staticmethod
    def _metadata_dict(metadata: Mapping[str, Any] | str | None) -> dict[str, Any]:
        if isinstance(metadata, Mapping):
            return dict(metadata)

        if isinstance(metadata, str) and metadata:
            try:
                parsed = json.loads(metadata)
            except (TypeError, ValueError):
                return {"metadata": metadata}
            if isinstance(parsed, Mapping):
                return dict(parsed)

        return {}

    @staticmethod
    def _table_value(value: Any) -> str:
        if isinstance(value, (dict, list)):
            return json.dumps(value, ensure_ascii=False)
        return "" if value is None else str(value)
