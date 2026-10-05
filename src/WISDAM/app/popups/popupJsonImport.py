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
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see http://www.gnu.org/licenses/.
# ==============================================================================

from __future__ import annotations

from PySide6.QtCore import QPoint, Qt
from PySide6.QtGui import QMouseEvent, QPixmap
from PySide6.QtWidgets import (
    QDialog,
    QFrame,
    QHBoxLayout,
    QLabel,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
)


class POPUPJsonImport(QDialog):
    def __init__(
        self,
        title: str,
        message: str,
        accept_text: str | None = None,
        cancel_text: str = "Cancel",
        parent=None,
    ):
        super().__init__(parent)
        self._drag_start: QPoint | None = None

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(640, 460)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        self.frame_main = QFrame(self)
        self.frame_main.setObjectName("frame_main")
        frame_layout = QVBoxLayout(self.frame_main)
        frame_layout.setContentsMargins(0, 0, 0, 0)
        frame_layout.setSpacing(0)
        layout.addWidget(self.frame_main)

        self.header = QFrame(self.frame_main)
        self.header.setObjectName("header")
        self.header.setMinimumHeight(42)
        self.header.setMaximumHeight(42)
        header_layout = QHBoxLayout(self.header)
        header_layout.setContentsMargins(10, 0, 12, 0)
        header_layout.setSpacing(10)
        frame_layout.addWidget(self.header)

        icon = QLabel(self.header)
        icon.setFixedSize(30, 30)
        icon.setPixmap(QPixmap(":/icons/icons/WISDAM_Icon_square_small.svg"))
        header_layout.addWidget(icon)

        self.title_label = QLabel(title, self.header)
        self.title_label.setObjectName("title_label")
        header_layout.addWidget(self.title_label)
        header_layout.addStretch(1)

        content = QFrame(self.frame_main)
        content.setObjectName("content")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(14, 14, 14, 14)
        content_layout.setSpacing(12)
        frame_layout.addWidget(content)

        self.message_text = QPlainTextEdit(content)
        self.message_text.setReadOnly(True)
        self.message_text.setPlainText(message)
        content_layout.addWidget(self.message_text)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)

        if accept_text is not None:
            self.accept_button = QPushButton(accept_text, content)
            self.accept_button.clicked.connect(self.accept)
            button_layout.addWidget(self.accept_button)

        self.cancel_button = QPushButton(cancel_text, content)
        self.cancel_button.clicked.connect(self.reject)
        button_layout.addWidget(self.cancel_button)
        content_layout.addLayout(button_layout)

        self.setStyleSheet(
            """
            QFrame#frame_main {
                background-color: rgb(34, 36, 50);
                color: rgb(210, 210, 210);
                border: 1px solid rgb(85, 50, 50);
            }
            QFrame#header {
                background-color: rgb(85, 50, 50);
                color: white;
                border: none;
            }
            QLabel#title_label {
                background: transparent;
                color: white;
                font: 700 10pt "Segoe UI";
            }
            QFrame#content {
                background-color: rgb(34, 36, 50);
                border: none;
            }
            QPlainTextEdit {
                background-color: rgb(27, 29, 35);
                color: rgb(210, 210, 210);
                border: 1px solid rgb(52, 59, 72);
                selection-background-color: rgb(85, 50, 50);
                padding: 8px;
                font: 9pt "Consolas";
            }
            QPushButton {
                color: rgb(210, 210, 210);
                border: 2px solid rgb(52, 59, 72);
                border-radius: 5px;
                background-color: rgb(52, 59, 72);
                padding: 5px 18px;
                min-width: 86px;
            }
            QPushButton:hover {
                background-color: rgb(57, 65, 80);
                border: 2px solid rgb(85, 50, 50);
            }
            QPushButton:pressed {
                background-color: rgb(35, 40, 49);
                border: 2px solid rgb(43, 50, 61);
            }
            QScrollBar:vertical {
                border: none;
                background: rgb(52, 59, 72);
                width: 14px;
                margin: 14px 0 14px 0;
            }
            QScrollBar::handle:vertical {
                background: rgb(85, 50, 50);
                min-height: 25px;
                border-radius: 7px;
            }
            QScrollBar::add-line:vertical,
            QScrollBar::sub-line:vertical {
                background: transparent;
                height: 14px;
            }
            """
        )

    def mousePressEvent(self, event: QMouseEvent) -> None:
        if event.button() == Qt.LeftButton and self.header.geometry().contains(
            event.position().toPoint()
        ):
            self._drag_start = (
                event.globalPosition().toPoint() - self.frameGeometry().topLeft()
            )
            event.accept()
            return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if self._drag_start is not None and event.buttons() & Qt.LeftButton:
            self.move(event.globalPosition().toPoint() - self._drag_start)
            event.accept()
            return
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self._drag_start = None
        super().mouseReleaseEvent(event)
