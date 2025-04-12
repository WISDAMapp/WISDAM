# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2025 Martin Wieser.
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


import geopandas as gpd
from PySide6.QtGui import QPen, QColor, QPainter, QPolygonF
from PySide6.QtCore import QPoint, Qt, QPointF
from PySide6.QtSvgWidgets import QGraphicsSvgItem
from PySide6.QtWidgets import (QApplication, QGraphicsItem, QGraphicsPolygonItem, QGraphicsView,
                               QGraphicsItemGroup)

from app.var_classes import Selection


class Node(QGraphicsSvgItem):

    def __init__(self, *args, **kwargs):
        QGraphicsSvgItem.__init__(self, *args, **kwargs)

        # we retrieve the pixmap based on the subtype to initialize a QGraphicsSvgItem
        self.setFlag(QGraphicsItem.ItemSendsScenePositionChanges, False)
        self.setFlag(QGraphicsItem.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.ItemIsMovable, False)
        self.setZValue(10)


class GISView(QGraphicsView):

    def __init__(self, parent=None):
        super(GISView, self).__init__(parent)

        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setRenderHints(QPainter.Antialiasing | QPainter.SmoothPixmapTransform)
        self.setMouseTracking(True)

        self._dragPos = QPoint()
        self.x_pos = 0
        self.y_pos = 0
        self.middlePressed = False

        self.ratio, self.offset = 1 / 400, (0, 0)

        # brush for water and lands
        # self.land_brush = QBrush(QColor(52, 165, 111))
        self.land_pen = QPen(QColor(20, 0, 0))
        self.land_pen.setWidth(0)

        self.item_earth: QGraphicsItemGroup = QGraphicsItemGroup()
        self.item_images_groups = []
        self.item_group_node = QGraphicsItemGroup()

    # self.draw_map()

    # draw the map
    def draw_map(self, path_to_data: str):
        self.item_earth = self.draw_land_shape(path_to_data)
        self.item_group_node = QGraphicsItemGroup()
        if self.item_group_node:
            if self.transform().m11() > 1000:
                self.item_group_node.hide()
        self.item_earth = self.scene().createItemGroup(self.item_earth)

    # Zoom system
    def zoom(self, f):

        if self.transform().m11() < 5000000 and f > 1:
            self.scale(f, f)
        if self.transform().m11() > 2 and f < 1:
            self.scale(f, f)

        if self.item_group_node:
            if self.transform().m11() > 1000:
                if self.item_group_node.isVisible():
                    self.item_group_node.hide()
            else:
                if not self.item_group_node.isVisible():
                    self.item_group_node.show()

    def wheelEvent(self, event):

        num_degrees = event.angleDelta().y() / 10  # event.delta() / 10 #
        num_steps = num_degrees / 15.0
        # self.centerOn(self.mapToScene(event.pos()))
        old_mouse_img_coo = self.mapToScene(event.position().toPoint())
        diff_vec = event.position() - QPointF(self.width() / 2, self.height() / 2)
        self.zoom(pow(0.8, num_steps))
        new_middle_map_pos = self.mapFromScene(old_mouse_img_coo).toPointF() - diff_vec
        self.centerOn(self.mapToScene(new_middle_map_pos.toPoint()))

    # Mouse bindings
    def mousePressEvent(self, event):

        self._dragPos = event.position()
        if event.buttons() == Qt.LeftButton:
            if self.scene().selection_mode == Selection.Rectangle:
                self.setDragMode(QGraphicsView.DragMode.RubberBandDrag)
            else:
                self.setDragMode(QGraphicsView.DragMode.NoDrag)
        if event.button() == Qt.MiddleButton:
            self.middlePressed = True
            QApplication.setOverrideCursor(Qt.ClosedHandCursor)
            self.setDragMode(QGraphicsView.DragMode.NoDrag)
        # if event.button() == Qt.RightButton:
        #    self.setDragMode(QGraphicsView.DragMode.NoDrag)
        super(GISView, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        if event.button() == Qt.MiddleButton:
            self.middlePressed = False
            QApplication.restoreOverrideCursor()
        super(GISView, self).mouseReleaseEvent(event)

    # Drag & Drop system

    def mouseMoveEvent(self, event):

        new_pos = event.position()
        if self.middlePressed:
            diff = new_pos - self._dragPos
            self._dragPos = new_pos
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - diff.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - diff.y())
            event.accept()
        super(GISView, self).mouseMoveEvent(event)

    def draw_land_shape(self, path_to_data: str):
        sf = gpd.read_file(path_to_data)
        poly_return = []
        for polygon in sf.geometry:
            # convert shapefile geometries into shapely geometries
            # to extract the polygons of a multipolygon

            # if it is a polygon, we use a list to make it iterable
            if polygon.geom_type == 'Polygon':
                polygon = [polygon]
            else:
                polygon = list(polygon.geoms)
            for land in polygon:
                qt_polygon = QPolygonF()
                for x, y in land.exterior.coords:
                    qt_polygon.append(QPointF(x, -y))
                polygon_item = QGraphicsPolygonItem(qt_polygon)
                # polygon_item.setBrush(self.land_brush)
                polygon_item.setPen(self.land_pen)
                polygon_item.setZValue(0)
                poly_return.append(polygon_item)
        return poly_return
