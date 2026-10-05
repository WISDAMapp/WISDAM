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


from shapely import geometry

from PySide6.QtCore import Qt, QPersistentModelIndex, QPointF, QRectF, QLineF
from PySide6.QtGui import (
    QBrush,
    QFont,
    QPen,
    QColor,
    QCursor,
    QPainterPath,
    QPainterPathStroker,
    QPolygonF,
)
from PySide6.QtWidgets import (
    QGraphicsRectItem,
    QGraphicsPolygonItem,
    QGraphicsEllipseItem,
    QGraphicsItem,
    QGraphicsPathItem,
    QGraphicsTextItem,
)
from app.var_classes import ColorGui


class RectangleAnnotation(QGraphicsRectItem):
    def __init__(
        self,
        parent=None,
        color=None,
        object_id=0,
        image_id=0,
        object_type=None,
        group_area=0,
        resight_set=0,
        projection=False,
        reviewed=1,
        source=0,
        pen_width=3,
        image_datetime=None,
    ):
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
        self.image_datetime = image_datetime
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
        self.setToolTip("")
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

        if (
            abs(pos.x() - rect_coords[0]) < distance
            or abs(pos.x() - rect_coords[2]) < distance
        ) and (
            abs(pos.y() - rect_coords[1]) < distance
            or abs(pos.y() - rect_coords[3]) < distance
        ):
            return True, 0
        return False, 0

    def is_valid(self):
        return True

    def get_coords(self, image_width, image_height):
        rect = self.rect()
        valid = (
            rect.x() >= 0
            and rect.y() >= 0
            and rect.x() + rect.width() <= image_width
            and rect.y() + rect.height() <= image_height
        )

        return [[p.x(), p.y()] for p in QPolygonF(rect).toList()], valid


class OctoLines:
    def __init__(self, x, y, pick_radius):
        self.line_list = [
            QLineF(
                QPointF(x, y + pick_radius),
                QPointF(x + pick_radius * 0.707, y + pick_radius * 0.707),
            ),
            QLineF(
                QPointF(x + pick_radius * 0.707, y + pick_radius * 0.707),
                QPointF(x + pick_radius, y),
            ),
            QLineF(
                QPointF(x + pick_radius, y),
                QPointF(x + pick_radius * 0.707, y - pick_radius * 0.707),
            ),
            QLineF(
                QPointF(x + pick_radius * 0.707, y - pick_radius * 0.707),
                QPointF(x, y - pick_radius),
            ),
            QLineF(
                QPointF(x, y - pick_radius),
                QPointF(x - pick_radius * 0.707, y - pick_radius * 0.707),
            ),
            QLineF(
                QPointF(x - pick_radius * 0.707, y - pick_radius * 0.707),
                QPointF(x - pick_radius, y),
            ),
            QLineF(
                QPointF(x - pick_radius, y),
                QPointF(x - pick_radius * 0.707, y + pick_radius * 0.707),
            ),
            QLineF(
                QPointF(x - pick_radius * 0.707, y + pick_radius * 0.707),
                QPointF(x, y + pick_radius),
            ),
        ]

    def intersect(self, line: QLineF):
        if hasattr(QLineF, "BoundedIntersection"):
            bounded_intersection = QLineF.BoundedIntersection
        else:
            bounded_intersection = QLineF.IntersectionType.BoundedIntersection

        for octo_line in self.line_list:
            inter_type, inter_p = line.intersects(octo_line)
            if inter_type == bounded_intersection:
                return True, inter_p
        return False, None

    def items(self):
        return self.line_list


class PointAnnotation(QGraphicsEllipseItem):
    def __init__(
        self,
        parent=None,
        color=None,
        object_id=0,
        image_id=0,
        object_type=None,
        group_area=0,
        resight_set=0,
        projection=False,
        reviewed=1,
        source=0,
        pen_width=5,
        image_datetime=None,
    ):
        super(PointAnnotation, self).__init__(parent)
        self.setZValue(10)
        self.setAcceptHoverEvents(True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, True)

        self.object_id = object_id
        self.image_id = image_id
        self.image_datetime = image_datetime

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

    def center(self):
        ellipse_rect = self.rect()
        return QPointF(
            ellipse_rect.x() + ellipse_rect.width() / 2.0,
            ellipse_rect.y() + ellipse_rect.height() / 2.0,
        )

    def move(self, vector):
        ellipse_rect = self.rect()
        self.setRect(
            ellipse_rect.x() + vector[0],
            ellipse_rect.y() + vector[1],
            ellipse_rect.width(),
            ellipse_rect.height(),
        )

    def get_coords(self, image_width, image_height):
        center = self.center()
        valid = 0 <= center.x() <= image_width and 0 <= center.y() <= image_height
        return [center.x(), center.y()], valid

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

        self.setToolTip("")
        super(PointAnnotation, self).hoverLeaveEvent(event)


class PathAnnotation(QGraphicsPathItem):
    def __init__(
        self,
        parent=None,
        color=None,
        object_id=0,
        image_id=0,
        object_type=None,
        group_area=0,
        resight_set=0,
        projection=False,
        reviewed=1,
        source=0,
        pen_width=3,
        stroke_buffer=10,
        image_datetime=None,
    ):
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
        self.image_datetime = image_datetime
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

    def point_list(self):
        path = self.path()
        return [QPointF(path.elementAt(idx)) for idx in range(path.elementCount())]

    def set_point_list(self, points):
        if not points:
            self.setPath(QPainterPath())
            return

        path = QPainterPath(points[0])
        for point in points[1:]:
            path.lineTo(point)
        self.setPath(path)

    def move(self, vector):
        points = [
            QPointF(point.x() + vector[0], point.y() + vector[1])
            for point in self.point_list()
        ]
        self.set_point_list(points)

    def change_geometry(self, pos, target_point=None):
        path = self.path()
        if target_point is not None and 0 <= target_point < path.elementCount():
            path.setElementPositionAt(target_point, pos.x(), pos.y())
            self.setPath(path)

    def get_coords(self, image_width, image_height):
        points = self.point_list()
        valid = len(points) >= 2
        for point in points:
            if (
                point.x() < 0
                or point.y() < 0
                or point.x() > image_width
                or point.y() > image_height
            ):
                valid = False
        return [[point.x(), point.y()] for point in points], valid

    def close_point(self, pos, distance):
        closest_idx = 0
        closest_distance = distance**2
        found = False

        for idx, point in enumerate(self.point_list()):
            dist = point - pos
            dist_squared = dist.x() ** 2 + dist.y() ** 2
            if dist_squared < closest_distance:
                closest_distance = dist_squared
                closest_idx = idx
                found = True
        return found, closest_idx

    def close_octo(self, octo: OctoLines):
        points = self.point_list()
        inter_p: QPointF | None = None
        for idx in range(len(points) - 1):
            valid, inter_p = octo.intersect(QLineF(points[idx], points[idx + 1]))
            if valid:
                return True, idx, inter_p

        return False, 0, inter_p

    def insert_point_after(self, target_point, pos):
        points = self.point_list()
        points.insert(target_point + 1, pos)
        self.set_point_list(points)
        return True

    def remove_point(self, target_point):
        points = self.point_list()
        if len(points) <= 2 or target_point < 0 or target_point >= len(points):
            return False

        del points[target_point]
        self.set_point_list(points)
        return True

    def is_valid(self):
        return self.path().elementCount() >= 2

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

        self.setToolTip("")
        super(PathAnnotation, self).hoverLeaveEvent(event)


class MeasurePathAnnotation(QGraphicsPathItem):
    def __init__(self, gsd: float, parent=None, color: str = "#c90ec3"):
        super(MeasurePathAnnotation, self).__init__(parent)

        self.gsd = gsd
        self.setZValue(1000)
        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        pen = QPen(QColor(color), 3)
        pen.setCosmetic(True)
        pen.setStyle(Qt.PenStyle.DashLine)
        self.setPen(pen)
        self.setBrush(Qt.transparent)

        self.label_background = QGraphicsPathItem(self)
        self.label_background.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        )
        self.label_background.setBrush(QBrush(QColor("white")))
        self.label_background.setPen(QPen(Qt.PenStyle.NoPen))
        self.label_background.setZValue(1000)

        self.label = QGraphicsTextItem(self)
        self.label.setFlag(
            QGraphicsItem.GraphicsItemFlag.ItemIgnoresTransformations, True
        )
        self.label.setDefaultTextColor(QColor(color))
        font = QFont()
        font.setBold(True)
        font.setPointSize(10)
        self.label.setFont(font)
        self.label.setZValue(1001)
        self.update_label()

    def setPath(self, path: QPainterPath):
        super(MeasurePathAnnotation, self).setPath(path)
        self.update_label()

    def update_label(self):
        length_m = self.path_length_px() * self.gsd
        self.label.setPlainText(self.format_length(length_m))

        path = self.path()
        if path.elementCount():
            pos = path.currentPosition() + QPointF(8, -28)
            self.label.setPos(pos)
            self.label_background.setPos(pos)
            self._update_label_background()

    def _update_label_background(self):
        padding_x = 2
        padding_y = 2
        rect = self.label.boundingRect().adjusted(
            -padding_x, -padding_y, padding_x, padding_y
        )
        background_path = QPainterPath()
        background_path.addRoundedRect(QRectF(rect), 5, 5)
        self.label_background.setPath(background_path)

    def path_length_px(self) -> float:
        path = self.path()
        length = 0.0

        if path.elementCount() < 2:
            return length

        first = path.elementAt(0)
        previous = QPointF(first.x, first.y)
        for index in range(1, path.elementCount()):
            element = path.elementAt(index)
            current = QPointF(element.x, element.y)
            delta = current - previous
            length += (delta.x() ** 2 + delta.y() ** 2) ** 0.5
            previous = current

        return length

    @staticmethod
    def format_length(length_m: float) -> str:
        if length_m >= 1000.0:
            return f"{length_m / 1000.0:.2f} km"
        if length_m >= 10.0:
            return f"{length_m:.1f} m"
        return f"{length_m:.2f} m"


class PolygonAnnotation(QGraphicsPolygonItem):
    def __init__(
        self,
        parent=None,
        color=None,
        object_id=0,
        image_id=0,
        object_type=None,
        group_area=0,
        resight_set=0,
        projection=False,
        reviewed=1,
        source=0,
        pen_width=3,
        image_datetime=None,
    ):
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
        self.image_datetime = image_datetime
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

    # def setPolygon(self, polygon) -> None:
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

    @staticmethod
    def _points_equal(p1: QPointF, p2: QPointF):
        return (p1 - p2).manhattanLength() < 0.01

    def _normalized_points(self):
        points = self.polygon().toList()
        if len(points) > 1 and self._points_equal(points[0], points[-1]):
            points = points[:-1]
        return points

    def _set_points(self, points):
        poly = QPolygonF(points)
        if points:
            poly.append(points[0])
        self.setPolygon(poly)

    def move(self, vector):
        points = [
            QPointF(point.x() + vector[0], point.y() + vector[1])
            for point in self._normalized_points()
        ]
        self._set_points(points)

    def change_geometry(self, pos, target_point=None):
        points = self._normalized_points()
        if target_point is None or target_point < 0 or target_point >= len(points):
            return

        old_point = points[target_point]
        points[target_point] = pos
        if self._points_valid(points):
            self._set_points(points)
        else:
            points[target_point] = old_point

    def get_coords(self, image_width, image_height):
        points = self._normalized_points()
        valid = self._points_valid(points)
        for point in points:
            if (
                point.x() < 0
                or point.y() < 0
                or point.x() > image_width
                or point.y() > image_height
            ):
                valid = False

        coords = [[point.x(), point.y()] for point in points]
        if coords:
            coords.append(coords[0])
        return coords, valid

    def close_point(self, pos, distance):
        closest_idx = 0
        closest_distance = distance**2
        found = False

        for idx, point in enumerate(self._normalized_points()):
            dist = point - pos
            dist_squared = dist.x() ** 2 + dist.y() ** 2
            if dist_squared < closest_distance:
                closest_distance = dist_squared
                closest_idx = idx
                found = True

        return found, closest_idx

    def close_octo(self, octo: OctoLines):
        inter_p: QPointF | None = None
        points = self._normalized_points()
        if len(points) < 2:
            return False, 0, inter_p

        closed_points = points + [points[0]]
        for idx in range(len(points)):
            valid, inter_p = octo.intersect(
                QLineF(closed_points[idx], closed_points[idx + 1])
            )
            if valid:
                return True, idx, inter_p

        return False, 0, inter_p

    def insert_point_after(self, target_point, pos):
        points = self._normalized_points()
        points.insert(target_point + 1, pos)
        if self._points_valid(points):
            self._set_points(points)
            return True
        return False

    def remove_point(self, target_point):
        points = self._normalized_points()
        if len(points) <= 3 or target_point < 0 or target_point >= len(points):
            return False

        old_points = points[:]
        del points[target_point]
        if self._points_valid(points):
            self._set_points(points)
            return True

        self._set_points(old_points)
        return False

    @staticmethod
    def _points_valid(points):
        if len(points) < 3:
            return False
        coords = [[point.x(), point.y()] for point in points]
        return geometry.Polygon(coords).is_valid

    def is_valid(self):
        return self._points_valid(self._normalized_points())

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

        self.setToolTip("")
        super(PolygonAnnotation, self).hoverLeaveEvent(event)


class PolygonFootprint(QGraphicsPolygonItem):
    def __init__(
        self,
        parent=None,
        color=None,
        image_id=0,
        group_image=0,
        folder="",
        inspected: int = 0,
        transect="",
        block_id="",
        flight_ref="",
    ):
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

    # def hoverEnterEvent(self, event):
    #    self.setBrush(ColorGui.color_on_image_hoover)
    #    p = QPen(QColor("green"), 0)
    #    p.setCosmetic(True)
    #    self.setPen(p)
    #    super(PolygonFootprint, self).hoverEnterEvent(event)

    # def hoverLeaveEvent(self, event):
    #    p = QPen(self.color, 0)
    #    p.setCosmetic(True)
    #    self.setPen(p)
    #    c1 = self.color
    #    c1.setAlpha(20)
    #    self.setBrush(c1)
    #    super(PolygonFootprint, self).hoverLeaveEvent(event)


class PointCenterpoint(QGraphicsEllipseItem):
    def __init__(
        self,
        parent=None,
        color=None,
        image_id=0,
        group_image=0,
        folder="",
        inspected: int = 0,
        transect="",
        block_id="",
        flight_ref="",
        persistent_index: QPersistentModelIndex | None = None,
    ):
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

        if not self.scene().hide_footprints_on_hover_flag:
            self.childItems()[0].setVisible(True)

        super(PointCenterpoint, self).hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        p = QPen(self.color_pen, 0)
        p.setCosmetic(True)
        self.setPen(p)
        self.setBrush(self.color_brush)

        if not self.scene().show_images_flag:
            self.childItems()[0].setVisible(False)
        super(PointCenterpoint, self).hoverLeaveEvent(event)


class PathImages(QGraphicsPathItem):
    def __init__(
        self,
        parent=None,
        color=None,
        object_id=0,
        image_id=0,
        object_type=None,
        group_area=0,
        resight_set=0,
        projection=False,
        reviewed=1,
        source=0,
        pen_width=0,
        stroke_buffer=10,
    ):
        super(PathImages, self).__init__(parent)
        self.setZValue(0)

        self.setAcceptHoverEvents(False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable, False)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemSendsGeometryChanges, False)

        p = QPen(QColor(100, 100, 100, 100), pen_width)
        self.setPen(p)


class SelectionPolygon(QGraphicsPolygonItem):
    def __init__(
        self,
    ):
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
    def __init__(
        self,
    ):
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
        # p.setStyle(Qt.PenStyle.DotLine)
        self.setPen(p)
        self.setBrush(Qt.transparent)
