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


from PySide6 import QtWidgets
from PySide6.QtCore import Qt, Signal
from PySide6.QtGui import QColor
from PySide6.QtWidgets import QColorDialog


def stylesheet_parser_colorclass(color):

	text = 'QPushButton {border: 4px solid '
	text += color.name() + '; border-radius: 5px;background-color: '
	text += color.name(QColor.HexArgb) + ';}\n'
	text += "QPushButton:hover {background-color: rgba(0, 255, 0,50);border: 4px solid rgb(35, 230, 32);}"

	return text


class ColorButton(QtWidgets.QPushButton):
	"""
	Custom Qt Widget to show a chosen color on a button.
	If Button is pressed the color chooser will open
	"""

	colorChanged = Signal(QColor)

	def __init__(self, *args, color=None, **kwargs):
		super(ColorButton, self).__init__(*args, **kwargs)

		self._color = None
		self.dialogue_color = None
		self._default = color
		self.pressed.connect(self.on_color_picker)

	def set_color(self, color):
		if color != self._color:
			self._color = color

		if self._color:
			self.setStyleSheet(stylesheet_parser_colorclass(self._color))
		else:
			self.setStyleSheet("")

	def color(self):
		return self._color

	def on_color_picker(self):
		"""
		Show color-picker dialog to select color.
		Qt will use the native dialog by default.
		"""
		dlg = QColorDialog()
		dlg.setOption(QColorDialog.ColorDialogOption.ShowAlphaChannel, True)
		if not self.dialogue_color:
			self.dialogue_color = dlg.currentColor()
		else:
			dlg.setCurrentColor(self.dialogue_color)

		color = dlg.getColor(options=QColorDialog.ColorDialogOption.ShowAlphaChannel)
		if color.isValid():
			if color.alpha() == 255:
				color.setAlpha(150)
			self.set_color(color)
			self.colorChanged.emit(color)

	def mousePressEvent(self, e):
		if e.button() == Qt.RightButton:
			self.set_color(self._default)

		return super(ColorButton, self).mousePressEvent(e)
