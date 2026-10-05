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


import re

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QSizePolicy,
    QToolButton,
    QVBoxLayout,
    QWidget,
)


class AccordionSection(QWidget):
    def __init__(
        self, title: str, content: QWidget, has_indicator: bool = False, parent=None
    ):
        super().__init__(parent)

        self.content = content
        self.indicator = None

        self.header = QToolButton(self)
        self.header.setText(title)
        self.header.setCheckable(True)
        self.header.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.header.setArrowType(Qt.ArrowType.NoArrow)
        self.header.setToolButtonStyle(Qt.ToolButtonStyle.ToolButtonTextBesideIcon)
        self.header.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed
        )
        self.header.setMinimumHeight(32)
        self.header.setStyleSheet(self._header_style())

        if has_indicator:
            self.indicator = QLabel(self.header)
            self.indicator.setFixedSize(13, 13)
            self.indicator.setToolTip("Active setting")
            self.indicator.setAttribute(
                Qt.WidgetAttribute.WA_TransparentForMouseEvents, True
            )
            self.indicator.setStyleSheet("""
                QLabel {
                    background-color: rgb(76, 175, 80);
                    border-radius: 6px;
                }
            """)
            self.indicator.hide()

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(4)
        layout.addWidget(self.header)
        layout.addWidget(self.content)

        self.set_open(False)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self._position_indicator()

    def set_open(self, open_: bool):
        self.header.setChecked(open_)
        self.header.setArrowType(Qt.ArrowType.NoArrow)
        #    Qt.ArrowType.DownArrow if open_ else Qt.ArrowType.RightArrow
        # )
        self.content.setVisible(open_)

    def set_indicator_active(self, active: bool):
        if self.indicator is None:
            return

        self.indicator.setVisible(active)
        self._position_indicator()

    def _position_indicator(self):
        if self.indicator is None:
            return

        self.indicator.move(
            self.header.width() - self.indicator.width() - 12,
            (self.header.height() - self.indicator.height()) // 2,
        )
        self.indicator.raise_()

    def _header_style(self) -> str:
        color = self._content_background_color()
        return f"""
            QToolButton {{
                background-color: {color};
                border: 0px;
                border-radius: 5px;
                color: white;
                font-size: 12pt;
                font-weight: bold;
                padding: 5px;
                text-align: center;
            }}
            QToolButton:hover {{
                border: 2px solid rgb(61, 70, 86);
            }}
        """

    def _content_background_color(self) -> str:
        color = self.content.property("accordionColor")
        if color:
            return str(color)

        match = re.search(
            r"background(?:-color)?\s*:\s*([^;}]+)", self.content.styleSheet()
        )
        if match:
            return match.group(1).strip()

        return "rgb(52, 59, 72)"


class AccordionFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)

        self._sections: list[AccordionSection] = []
        self._sections_by_object_name: dict[str, AccordionSection] = {}
        self._pending_indicator_states: dict[str, bool] = {}
        self._initialized = False

        # Designer children are added after this __init__, so delay setup.
        QTimer.singleShot(0, self.setup_accordion)

    def setup_accordion(self):
        if self._initialized:
            return
        self._initialized = True

        children = [
            child
            for child in self.findChildren(
                QWidget,
                options=Qt.FindChildOption.FindDirectChildrenOnly,
            )
            if not isinstance(child, AccordionSection)
        ]

        children.sort(key=self._child_order)

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 10, 0, 0)
        layout.setSpacing(8)

        default_section = None

        for child in children:
            title = child.property("accordionTitle") or child.objectName()

            child.setParent(self)

            section = AccordionSection(
                str(title),
                child,
                self._property_is_true(child.property("accordionIndicator")),
                self,
            )
            section.header.clicked.connect(
                lambda checked=False, active_section=section: self.toggle_section(
                    active_section, checked
                )
            )

            self._sections.append(section)
            self._sections_by_object_name[child.objectName()] = section
            layout.addWidget(section)

            if child.objectName() in self._pending_indicator_states:
                section.set_indicator_active(
                    self._pending_indicator_states[child.objectName()]
                )

            if self._is_default_open(child):
                default_section = section

        layout.addStretch(1)

        if default_section is not None:
            self.set_current_section(default_section)
        elif self._sections:
            self.set_current_section(self._sections[0])

    @staticmethod
    def _child_order(child: QWidget) -> int:
        order = child.property("accordionOrder")

        try:
            return int(order)
        except (TypeError, ValueError):
            return 9999

    @staticmethod
    def _is_default_open(child: QWidget) -> bool:
        return AccordionFrame._property_is_true(child.property("accordionDefaultOpen"))

    @staticmethod
    def _property_is_true(value) -> bool:
        if value is True:
            return True
        if isinstance(value, str):
            return value.lower() in {"1", "true", "yes", "on"}
        return False

    def set_section_indicator(self, object_name: str, active: bool):
        self._pending_indicator_states[object_name] = active

        section = self._sections_by_object_name.get(object_name)
        if section is None:
            return

        section.set_indicator_active(active)

    def set_widget_section_indicator(self, widget: QWidget, active: bool):
        for section in self._sections:
            if widget is section.content or section.content.isAncestorOf(widget):
                self.set_section_indicator(section.content.objectName(), active)
                return

        section_content = widget
        while section_content is not None:
            if section_content.parentWidget() is self:
                self.set_section_indicator(section_content.objectName(), active)
                return
            section_content = section_content.parentWidget()

    def toggle_section(self, active_section: AccordionSection, checked: bool):
        if checked:
            self.set_current_section(active_section)
        else:
            self.collapse_all()

    def collapse_all(self):
        for section in self._sections:
            section.set_open(False)

    def set_current_section(self, active_section: AccordionSection):
        for section in self._sections:
            section.set_open(section is active_section)
