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

from PySide6.QtCore import Signal, Qt, QRect, QPointF
from PySide6.QtGui import QPolygonF, QPainterPath
from PySide6.QtWidgets import (QGraphicsScene, QMenu, QGraphicsPixmapItem, QApplication)

from app.graphic.itemsGrahpicScene import RectangleAnnotation, PointAnnotation, PolygonAnnotation, PathAnnotation
from app.utils_qt import (create_tooltip_objects, list_of_points_to_list,
                          crop_image, create_tooltip_cropped_image)
from app.graphic.items_coloring import color_objects_attribute
from app.var_classes import (Instructions, point_size)

from db.dbHandler import DBHandler


class ImageScene(QGraphicsScene):
    show_popup = Signal(int)
    resight_set = Signal(list, bool)
    element_created = Signal(int, str, list)

    # group_clear_resight = Signal(list)

    def __init__(self, parent=None):
        super(ImageScene, self).__init__(parent)

        self.image_item: QGraphicsPixmapItem = QGraphicsPixmapItem()
        self.image_id_db: int | None = None
        self.db: DBHandler | None = None

        self.context_menu = QMenu()

        self.current_instruction = Instructions.No_Instruction
        self.working_instruction = False
        self.standard_color = '#000000'

        self.polygon_item: None | PolygonAnnotation = None
        self.p1_poly: None | PointAnnotation = None
        self.rectangle_item: None | RectangleAnnotation = None
        self.path_item: None | PathAnnotation = None

    def helpEvent(self, event):

        current_item = self.items(event.scenePos())

        if self.image_item in current_item:
            current_item.remove(self.image_item)

        if current_item:
            item_top: PolygonAnnotation | PointAnnotation | RectangleAnnotation | PathAnnotation = current_item[0]
            tooltip = None
            if item_top.projection:
                cropped_image = self.db.get_cropped_image(item_top.object_id)
                if cropped_image:
                    if cropped_image['cropped_image']:
                        tooltip = create_tooltip_cropped_image(cropped_image['cropped_image'], item_top.image_id,
                                                               item_top.object_type,
                                                               item_top.resight_set, item_top.source, item_top.reviewed)
            if not tooltip:
                tooltip = create_tooltip_objects(item_top.image_id,
                                                 item_top.object_type,
                                                 item_top.resight_set, item_top.source, item_top.reviewed)
            current_item[0].setToolTip(tooltip)

        super(ImageScene, self).helpEvent(event)

    def clear_scene(self):

        if self.items():
            self.clear()
            self.working_instruction = False

    # Emit signal to main to store Object into database
    def store_sightings(self, rectangle: QRect, geom_type: str, coords: list):

        if geom_type == 'Point':
            points_image = [coords[0].x(), coords[0].y()]
            geom = geometry.Point(points_image)

        elif geom_type == 'LineString':
            points_image = list_of_points_to_list(coords)
            geom = geometry.LineString(points_image)

        else:
            points_image = list_of_points_to_list(coords)
            geom = geometry.Polygon(points_image)

        pixmap_bytes = crop_image(self.image_item.pixmap(), rectangle)

        geojson = geometry.mapping(geom)
        obj_id = self.db.create_object(self.image_id_db, geojson=geojson, cropped_image=pixmap_bytes)
        # tooltip = create_tooltip_objects(self.image_id_db, 'None', 0, reviewed=1, source=0)

        self.element_created.emit(obj_id, geom_type, points_image)

        return obj_id

    def delete_object(self, item_id):
        for item in self.items():
            if hasattr(item, 'object_id'):
                if item.object_id == item_id:
                    self.removeItem(item)

    def change_object_type(self, item_list, object_type):
        # self.m_scene2.working_instruction = False
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.object_type = object_type
                        obj.reviewed = 1

    def change_reviewed(self, item_list: list[int]):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.reviewed = 1

    #TODO that functions are same for GIS, could be provided at one module
    def change_resight_set(self, item_list, group_index):
        # self.m_scene2.working_instruction = False
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.resight_set = group_index

    # def change_tooltip(self, item_ids, object_type=None, resight_set=None,
    # None):
    #    for item in self.items():
    #        if hasattr(item, 'object_id'):
    #            if item.object_id in item_ids:
    #                new_html = change_tooltip_html(item.toolTip(), object_type, resight_set, reviewed)
    #                item.setToolTip(new_html)

    def color_objects(self, attribute: str = None, color_dict: dict | None = None,
                      default_value=None, default_dict: dict | None = None):

        scene_items = [x for x in self.items() if x.__class__ in [PolygonAnnotation,
                                                                  PointAnnotation, RectangleAnnotation, PathAnnotation]]
        color_dict_new = None
        if scene_items:
            color_dict_new = color_objects_attribute(scene_items, attribute, color_dict=color_dict,
                                                     default_value=default_value, default_dict=default_dict)

        return color_dict_new

    def mouseDoubleClickEvent(self, event):
        if not self.working_instruction and event.button() == Qt.MouseButton.LeftButton:
            current_item = self.items(event.scenePos())
            if self.image_item in current_item:
                current_item.remove(self.image_item)
            if current_item:
                self.show_popup.emit(current_item[0].object_id)

    def mousePressEvent(self, event):

        modifiers = QApplication.queryKeyboardModifiers()
        current_item = self.items(event.scenePos())
        if self.image_item in current_item:

            # Remove image form items. Only geometries are left in current items list
            current_item.remove(self.image_item)

            # -----------------------------------------------------------------------------------------------
            # STACK CHANGE
            if len(current_item) > 1 and not self.working_instruction and event.button() == Qt.MouseButton.MiddleButton:
                current_item[0].stackBefore(current_item[-1])

            # -----------------------------------------------------------------------------------------------
            # Group Re-sightings for selected Items by popup Menu
            if self.selectedItems() and not self.working_instruction and \
                    event.button() == Qt.MouseButton.RightButton and modifiers == Qt.KeyboardModifier.ControlModifier:
                if len(self.selectedItems()) > 0:
                    self.context_menu = QMenu()

                    if len(self.selectedItems()) > 1:
                        text = "Resight Set"
                        resight_set = self.context_menu.addAction(text)
                        selected_index = [x.object_id for x in self.selectedItems()]
                        resight_set.triggered.connect(lambda: self.resight_set.emit(selected_index, False))

                    elif len(self.selectedItems()) == 1:
                        text = "Clear Resight Set"
                        group_clear_resight = self.context_menu.addAction(text)
                        selected_index = [x.object_id for x in self.selectedItems()]
                        group_clear_resight.triggered.connect(lambda: self.resight_set.emit(selected_index, True))

                    global_pos = event.screenPos()
                    self.context_menu.popup(global_pos)

            # -----------------------------------------------------------------------------------------------
            # Drawing instructions
            if not self.selectedItems():

                # POINT PICKING
                if self.current_instruction == Instructions.Point_Instruction \
                        and event.button() == Qt.MouseButton.RightButton:
                    point_item = PointAnnotation(color=self.standard_color,
                                                 image_id=self.image_id_db)
                    point_item.setRect(event.scenePos().x() - point_size / 2.0,
                                       event.scenePos().y() - point_size / 2.0,
                                       point_size, point_size)
                    self.working_instruction = False
                    coordinates = [event.scenePos().x(), event.scenePos().y()]
                    point_item.object_id = self.store_sightings(
                        QRect(int(coordinates[0]) - 25, int(coordinates[1]) - 25, 50, 50),
                        'Point', [event.scenePos()])
                    # point_item.setToolTip(tooltip)
                    self.addItem(point_item)

                # -----------------------------------------------------------------------------------------------
                # Rectangular and Polygon Picking starting
                if not self.working_instruction:

                    # Polygon
                    if self.current_instruction == Instructions.Polygon_Instruction:
                        if event.button() == Qt.RightButton:
                            # starting point of polygon will be show
                            self.p1_poly = PointAnnotation(color=self.standard_color)
                            self.addItem(self.p1_poly)
                            self.p1_poly.setRect(event.scenePos().x() - point_size / 2.0,
                                                 event.scenePos().y() - point_size / 2.0,
                                                 point_size, point_size)

                            self.polygon_item = PolygonAnnotation(color=self.standard_color,
                                                                  image_id=self.image_id_db)
                            self.addItem(self.polygon_item)
                            self.working_instruction = True
                            self.polygon_item.setPolygon(QPolygonF())
                            poly = self.polygon_item.polygon()
                            poly.append(event.scenePos())
                            self.polygon_item.setPolygon(poly)

                    # Path
                    if self.current_instruction == Instructions.LineString_Instruction:
                        if event.button() == Qt.MouseButton.RightButton:
                            self.path_item = PathAnnotation(color=self.standard_color,
                                                            image_id=self.image_id_db)
                            self.addItem(self.path_item)

                            path = QPainterPath(event.scenePos())
                            path.lineTo(event.scenePos().x() + 1, event.scenePos().y() + 1)
                            self.path_item.setPath(path)
                            self.working_instruction = True

                    # Rectangle
                    if self.current_instruction == Instructions.Rectangle_Instruction:
                        if event.button() == Qt.MouseButton.RightButton:
                            self.rectangle_item = RectangleAnnotation(color=self.standard_color,
                                                                      image_id=self.image_id_db)
                            self.addItem(self.rectangle_item)
                            self.rectangle_item.start_rectangle(event.scenePos())
                            self.working_instruction = True

                # Continue with Polygon objects
                else:
                    if self.current_instruction == Instructions.Polygon_Instruction:

                        # Finish polygon objects
                        if event.button() == Qt.MouseButton.LeftButton:
                            self.working_instruction = False
                            if self.polygon_item.polygon().length() > 2:
                                rect = self.polygon_item.polygon().boundingRect().toRect()
                                coords = self.polygon_item.polygon().toList()
                                self.polygon_item.object_id = self.store_sightings(rect, 'Polygon', coords)
                                # self.polygon_item.setToolTip(tooltip)
                            else:
                                self.removeItem(self.polygon_item)
                            self.removeItem(self.p1_poly)

                        # Continue Polygon
                        elif event.button() == Qt.MouseButton.RightButton:

                            poly = self.polygon_item.polygon()
                            poly.append(event.scenePos())
                            self.polygon_item.setPolygon(poly)

                    if self.current_instruction == Instructions.LineString_Instruction:

                        # Finish path objects
                        if event.button() == Qt.MouseButton.LeftButton:
                            self.working_instruction = False
                            path = self.path_item.path()
                            coords = []
                            for idx in range(path.elementCount()):
                                coords.append(QPointF(path.elementAt(idx)))
                            rect = self.path_item.boundingRect().toRect()
                            self.path_item.object_id = self.store_sightings(rect, 'LineString', coords)
                            # self.path_item.setToolTip(tooltip)

                        # Continue Path
                        elif event.button() == Qt.MouseButton.RightButton:

                            path = self.path_item.path()
                            pos_new = event.scenePos()
                            if path.currentPosition() == pos_new:
                                pos_new = pos_new + QPointF(1, 1)
                            path.lineTo(pos_new)
                            self.path_item.setPath(path)

                    # Finish Rectangle
                    if self.current_instruction == Instructions.Rectangle_Instruction:
                        # Finish Rectangle
                        if event.button() == Qt.MouseButton.RightButton:
                            self.working_instruction = False
                            rect = self.rectangle_item.rect().toRect()
                            coords = QPolygonF(self.rectangle_item.rect()).toList()
                            self.rectangle_item.object_id = self.store_sightings(rect, 'Polygon', coords)
                            # self.rectangle_item.setToolTip(tooltip)
        # -----------------------------------------------------------------------------------------------
        # geometry outside of image due too projection
        else:
            # Stacking of sightings with Middle Button
            if len(current_item) > 1 and not self.working_instruction and event.button() == Qt.MouseButton.MiddleButton:
                current_item[0].stackBefore(current_item[-1])

        # -----------------------------------------------------------------------------------------------
        # Pass Event
        super(ImageScene, self).mousePressEvent(event)

    # -----------------------------------------------------------------------------------------------
    # If drawing is active for polygon or rectangle visually show the dynamic outlines
    def mouseMoveEvent(self, event):
        current_item = self.items(event.scenePos())

        # This tests if the mouse is within image borders
        if self.image_item in current_item:

            if self.working_instruction:

                # Polygon
                if self.current_instruction == Instructions.Polygon_Instruction:
                    poly = self.polygon_item.polygon()
                    if poly.length() > 2:
                        poly.removeLast()
                        poly.append(event.scenePos())
                        self.polygon_item.setPolygon(poly)

                # Path
                if self.current_instruction == Instructions.LineString_Instruction:
                    path = self.path_item.path()
                    idx = path.elementCount() - 1
                    path.setElementPositionAt(idx, event.scenePos().x(), event.scenePos().y())
                    self.path_item.setPath(path)

                # Rectangle
                if self.current_instruction == Instructions.Rectangle_Instruction:
                    self.rectangle_item.resize_rectangle(event.scenePos())

        super(ImageScene, self).mouseMoveEvent(event)
