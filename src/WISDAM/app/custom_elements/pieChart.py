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


from collections import namedtuple

from PySide6 import QtCore, QtGui
from PySide6 import QtCharts


class PieChartWisdam(QtCharts.QChart):

    def __init__(self, parent=None):

        super(PieChartWisdam, self).__init__(parent)
        self.offset = 140
        font = QtGui.QFont()
        font.setPointSize(12)

        self.setMargins(QtCore.QMargins(0, 0, 0, 0))

        # self.setTheme(QtCharts.QChart.ChartTheme.ChartThemeQt)
        self.setAnimationOptions(QtCharts.QChart.AnimationOption.SeriesAnimations)
        self.setBackgroundVisible(False)
        self.setPlotArea(QtCore.QRectF())
        self.slices = QtCharts.QPieSeries()
        self.slices.setHoleSize(0.35)
        self.slices.setPieStartAngle(self.offset)
        self.slices.setPieEndAngle(self.offset + 360)

        self.addSeries(self.slices)
        self.legend().setFont(font)
        self.legend().setAlignment(QtCore.Qt.AlignmentFlag.AlignRight)
        self.legend().setMarkerShape(QtCharts.QLegend.MarkerShape.MarkerShapeRectangle)
        self.legend().setLabelColor(QtGui.QColor(190, 190, 190))

    def clear(self):
        """Clear all slices in the pie chart
        """
        for slice_ in self.slices.slices():
            self.slices.take(slice_)

    def add_slice(self, label, value, color, values_max):

        font = QtGui.QFont()
        font.setPointSize(12)

        slice_item = QtCharts.QPieSlice(label, value)
        slice_item.setColor(QtGui.QColor(*color))
        slice_item.setPen(QtGui.QPen(QtCore.Qt.PenStyle.NoPen))
        slice_item.setLabelBrush(QtGui.QColor(190, 190, 190))
        slice_item.hovered.connect(slice_item.setExploded)
        if value/values_max < 0.05:
            slice_item.hovered.connect(slice_item.setLabelVisible)
        else:
            slice_item.setLabelVisible(True)
        slice_item.setExplodeDistanceFactor(0.1)
        slice_item.setLabelArmLengthFactor(0.1)
        slice_item.setLabelFont(font)
        self.slices.append(slice_item)


class CustomChartView(QtCharts.QChartView):
    """
    wrapper to be used as holder for ui file
    """

    def __init__(self, chart):
        super(CustomChartView, self).__init__(chart)

        self.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
