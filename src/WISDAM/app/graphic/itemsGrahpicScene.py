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


from PySide6.QtCore import Qt, QPersistentModelIndex
from PySide6.QtGui import (QPen, QColor, QCursor, QPainterPathStroker)
from PySide6.QtWidgets import (QGraphicsRectItem, QGraphicsPolygonItem, QGraphicsEllipseItem,
                               QGraphicsItem, QGraphicsPathItem, QGraphicsTextItem)
from app.var_classes import ColorGui


class RectangleAnnotation(QGraphicsRectItem):
    def __init__(self, parent=None, color=None, object_id=0, image_id=0, object_type=None, group_area=0,
                 resight_set=0, projection=False, reviewed=1, source=0, pen_width=3):
        super(RectangleAnnotation, self).__init__(parent)
        self.start_point_x = 0
        self.start_point_y = 0
        self.start = True
        self.setZValue(10)

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.object_id = object_id
        self.image_id = image_id
        self.projection = projection
        self.reviewed = reviewed
        self.source = source

        self.object_type = object_type

        self.group_area = group_area
        self.resight_set = resight_set

        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        self.pen_width = pen_width
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    def set_color(self, color):
        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    def hoverEnterEvent(self, event):
        self.setBrush(ColorGui.color_on_image_hoover)
        p = QPen(QColor("green"), self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        super(RectangleAnnotation, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.color)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setToolTip('')
        super(RectangleAnnotation, self).hoverLeaveEvent(event)

    def start_rectangle(self, p):
        self.start_point_x = p.x()
        self.start_point_y = p.y()

    def resize_rectangle(self, pos):
        if self.start_point_x != 0:
            width = abs(self.start_point_x - pos.x())
            height = abs(self.start_point_y - pos.y())
            start_point_new_x = self.start_point_x
            start_point_new_y = self.start_point_y
            if self.start_point_x > pos.x():
                start_point_new_x = pos.x()
            if self.start_point_y > pos.y():
                start_point_new_y = pos.y()
            self.setRect(start_point_new_x, start_point_new_y, width, height)

    def move(self, vector):
        rect = self.rect()

        x = rect.x() + vector[0]
        y = rect.y() + vector[1]

        self.setRect(x, y, rect.width(), rect.height())

    def change_geometry(self, pos, target_point=None):

        rect = self.rect()

        middle_x = rect.x() + rect.width() / 2
        middle_y = rect.y() + rect.height() / 2

        if pos.x() < middle_x:
            rect.setX(pos.x())
        # pass
        else:
            rect.setWidth(pos.x() - rect.x())

        if pos.y() < middle_y:
            rect.setY(pos.y())
        else:
            rect.setHeight(pos.y() - rect.y())

        self.setRect(rect)

    def close_point(self, pos, distance):

        rect_coords = self.rect().getCoords()

        if (abs(pos.x() - rect_coords[0]) < distance or
            abs(pos.x() - rect_coords[2]) < distance) and \
                (abs(pos.y() - rect_coords[1]) < distance or
                 abs(pos.y() - rect_coords[3]) < distance):
            return True, 0
        return False, 0

    def is_valid(self):
        return True


class PointAnnotation(QGraphicsEllipseItem):
    def __init__(self, parent=None, color=None, object_id=0, image_id=0, object_type=None, group_area=0,
                 resight_set=0, projection=False, reviewed=1, source=0, pen_width=5):
        super(PointAnnotation, self).__init__(parent)
        self.setZValue(10)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.object_id = object_id
        self.image_id = image_id

        self.object_type = object_type
        self.projection = projection
        self.group_area = group_area
        self.resight_set = resight_set
        self.reviewed = reviewed
        self.source = source

        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        self.pen_width = pen_width
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    def set_color(self, color):
        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    def hoverEnterEvent(self, event):
        self.setBrush(ColorGui.color_on_image_hoover)
        p = QPen(QColor("green"), self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        super(PointAnnotation, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.color)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)

        self.setToolTip('')
        super(PointAnnotation, self).hoverLeaveEvent(event)


class PathAnnotation(QGraphicsPathItem):

    def __init__(self, parent=None, color=None, object_id=0, image_id=0, object_type=None, group_area=0,
                 resight_set=0, projection=False, reviewed=1, source=0, pen_width=3, stroke_buffer=10):
        super(PathAnnotation, self).__init__(parent)
        self.start_point_x = 0
        self.start_point_y = 0
        self.start = True
        self.setZValue(10)

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.object_id = object_id
        self.image_id = image_id
        self.projection = projection
        self.reviewed = reviewed
        self.source = source
        self.object_type = object_type
        self.group_area = group_area
        self.resight_set = resight_set

        self.stroke_buffer = stroke_buffer
        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        self.pen_width = pen_width
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(Qt.transparent)

    def shape(self):

        qp = QPainterPathStroker()
        qp.setWidth(self.stroke_buffer)
        qp.setCapStyle(Qt.SquareCap)
        return qp.createStroke(self.path())

    def set_color(self, color):
        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(Qt.transparent)

    def hoverEnterEvent(self, event):
        self.setBrush(Qt.transparent)
        p = QPen(QColor("green"), self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        super(PathAnnotation, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(Qt.transparent)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)

        self.setToolTip('')
        super(PathAnnotation, self).hoverLeaveEvent(event)


class PolygonAnnotation(QGraphicsPolygonItem):
    def __init__(self, parent=None, color=None, object_id=0, image_id=0, object_type=None, group_area=0,
                 resight_set=0, projection=False, reviewed=1, source=0, pen_width=3):
        super(PolygonAnnotation, self).__init__(parent)
        self.m_points = []
        self.setZValue(10)

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.object_id = object_id
        self.image_id = image_id
        self.object_type = object_type
        self.projection = projection
        self.group_area = group_area
        self.resight_set = resight_set
        self.reviewed = reviewed
        self.source = source

        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        self.pen_width = pen_width
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    # So a text could be added
    # Snippet just for possible future usage
    #    self.textItem = QGraphicsTextItem(object_type, self)

    #def setPolygon(self, polygon) -> None:
    #    super(PolygonAnnotation, self).setPolygon(polygon)
    #    rect = self.textItem.boundingRect()
    #    rect.moveCenter(self.boundingRect().center())
    #    self.textItem.setPos(rect.topLeft())
    #    font = self.textItem.font()
    #    font.setPointSizeF(self.boundingRect().width()/10.0)
    #    self.textItem.setFont(font)

    def set_color(self, color):
        self.color = QColor(color)
        self.color.setAlpha(0)
        self.color_no_Alpha = QColor(color)
        self.color_no_Alpha.setAlpha(255)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color)

    def hoverEnterEvent(self, event):
        self.setBrush(ColorGui.color_on_image_hoover)
        p = QPen(QColor("green"), self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)
        super(PolygonAnnotation, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(self.color)
        p = QPen(self.color_no_Alpha, self.pen_width)
        p.setCosmetic(True)
        self.setPen(p)

        self.setToolTip('')
        super(PolygonAnnotation, self).hoverLeaveEvent(event)


class PolygonFootprint(QGraphicsPolygonItem):
    def __init__(self, parent=None, color=None, image_id=0, group_image=0, folder='',inspected: int =0,
                 transect='', block_id='', flight_ref=''):
        super(PolygonFootprint, self).__init__(parent)
        self.setZValue(0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        self.image_id = image_id

        self.group_image = group_image
        self.inspected = inspected
        self.folder = folder
        self.transect = transect
        self.flight_ref = flight_ref
        self.block = block_id

        self.color = QColor(color)
        self.setPen(QPen(self.color.toRgb(), 0))
        c1 = self.color
        c1.setAlpha(20)
        self.setBrush(c1)

    def set_color(self, color):
        self.color = QColor(color)
        self.setPen(QPen(self.color.toRgb(), 0))
        c1 = self.color
        c1.setAlpha(20)
        self.setBrush(c1)

    #def hoverEnterEvent(self, event):
    #    self.setBrush(ColorGui.color_on_image_hoover)
    #    p = QPen(QColor("green"), 0)
    #    p.setCosmetic(True)
    #    self.setPen(p)
    #    super(PolygonFootprint, self).hoverEnterEvent(event)

    #def hoverLeaveEvent(self, event):
    #    p = QPen(self.color, 0)
    #    p.setCosmetic(True)
    #    self.setPen(p)
    #    c1 = self.color
    #    c1.setAlpha(20)
    #    self.setBrush(c1)
    #    super(PolygonFootprint, self).hoverLeaveEvent(event)


class PointCenterpoint(QGraphicsEllipseItem):
    def __init__(self, parent=None, color=None, image_id=0, group_image=0, folder='', inspected: int = 0,
                 transect='', block_id='', flight_ref='', persistent_index: QPersistentModelIndex | None = None):
        super(PointCenterpoint, self).__init__(parent)
        self.setZValue(10)

        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))

        self.image_id = image_id

        self.group_image = group_image
        self.inspected = inspected
        self.folder = folder
        self.transect = transect
        self.flight_ref = flight_ref
        self.block = block_id
        self.persistent_index = persistent_index

        self.color_pen = QColor(color)
        self.color_pen.setAlpha(150)
        self.color_brush = QColor(color)
        self.color_brush.setAlpha(30)
        p = QPen(self.color_pen, 0)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color_brush)

    def set_color(self, color):
        self.color_pen = QColor(color)
        self.color_pen.setAlpha(150)
        self.color_brush = QColor(color)
        self.color_brush.setAlpha(30)
        p = QPen(self.color_pen, 0)
        p.setCosmetic(True)
        self.setPen(p)

        self.setBrush(self.color_brush)

    def hoverEnterEvent(self, event):
        self.setBrush(ColorGui.color_on_image_hoover)
        p = QPen(QColor("green"), 0)
        p.setCosmetic(True)
        self.setPen(p)

        if self.scene().show_footprints_on_hover_flag:
            self.childItems()[0].setVisible(True)

        super(PointCenterpoint, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        p = QPen(self.color_pen, 0)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color_brush)

        if self.scene().hide_images_flag:
            self.childItems()[0].setVisible(False)
        super(PointCenterpoint, self).hoverLeaveEvent(event)


class PathImages(QGraphicsPathItem):

    def __init__(self, parent=None, color=None, object_id=0, image_id=0, object_type=None, group_area=0,
                 resight_set=0, projection=False, reviewed=1, source=0, pen_width=0, stroke_buffer=10):
        super(PathImages, self).__init__(parent)
        self.setZValue(0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        p = QPen(QColor(100, 100, 100, 100), pen_width)
        self.setPen(p)


class SelectionPolygon(QGraphicsPolygonItem):
    def __init__(self, ):
        super(SelectionPolygon, self).__init__()
        self.setZValue(0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        p = QPen(QColor("#00A2E8"), 0)
        p.setCosmetic(True)
        p.setStyle(Qt.PenStyle.DotLine)
        self.setPen(p)
        c1 = QColor("#00A2E8")
        c1.setAlpha(20)
        self.setBrush(c1)


class GISNode(QGraphicsRectItem):
    def __init__(self, ):
        super(GISNode, self).__init__()
        self.setZValue(0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemStacksBehindParent, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        p = QPen(QColor("#AD3312"))
        p = QPen(QColor(159, 0, 0))
        p.setWidth(0)
        #p.setStyle(Qt.PenStyle.DotLine)
        self.setPen(p)
        self.setBrush(Qt.transparent)
