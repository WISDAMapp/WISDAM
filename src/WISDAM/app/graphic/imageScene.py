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


from datetime import datetime, timezone

from shapely import geometry

from PySide6.QtCore import Signal, Qt, QRect, QPointF
from PySide6.QtGui import QPolygonF, QPainterPath
from PySide6.QtWidgets import QGraphicsScene, QMenu, QGraphicsPixmapItem, QApplication

from app.graphic.itemsGrahpicScene import (
    RectangleAnnotation,
    PointAnnotation,
    PolygonAnnotation,
    PathAnnotation,
    MeasurePathAnnotation,
    OctoLines,
)
from app.utils_qt import (
    create_tooltip_objects,
    list_of_points_to_list,
    crop_image,
    create_tooltip_cropped_image,
)
from app.graphic.items_coloring import color_objects_attribute
from app.popups.popupConfirm import POPUPConfirm
from app.var_classes import Instructions, ObjectSourceList, point_size

from db.dbHandler import DBHandler


class ImageScene(QGraphicsScene):
    show_popup = Signal(int)
    resight_set = Signal(list, bool)
    element_created = Signal(int, str, list)
    element_changed = Signal(int, str, list)
    object_delete = Signal(int, int)

    # group_clear_resight = Signal(list)

    def __init__(self, parent=None):
        super(ImageScene, self).__init__(parent)

        self.image_item: QGraphicsPixmapItem = QGraphicsPixmapItem()
        self.image_id_db: int | None = None
        self.db: DBHandler | None = None

        self.context_menu = QMenu()

        self.current_instruction = Instructions.No_Instruction
        self.working_instruction = False
        self.standard_color = "#000000"

        self.polygon_item: None | PolygonAnnotation = None
        self.p1_poly: None | PointAnnotation = None
        self.rectangle_item: None | RectangleAnnotation = None
        self.path_item: None | PathAnnotation = None
        self.measure_item: None | MeasurePathAnnotation = None
        self.active_item: (
            None
            | RectangleAnnotation
            | PointAnnotation
            | PolygonAnnotation
            | PathAnnotation
        ) = None
        self.change_point_index = -1
        self.old_coords: QPointF | None = None
        self._original_geometry = None
        self.measure_gsd = 0.0
        self.image_datetime = None

    def set_object_visibility(
        self,
        hide_current_image: bool = False,
        hide_projections: bool = False,
        hidden_sources: set[int] | None = None,
    ):
        hidden_sources = hidden_sources or set()

        for obj in self.items():
            if not hasattr(obj, "projection"):
                continue

            visible = True
            if obj.projection and hide_projections:
                visible = False
            elif not obj.projection and hide_current_image:
                visible = False

            if hasattr(obj, "source") and obj.source in hidden_sources:
                visible = False

            obj.setVisible(visible)

    def helpEvent(self, event):

        current_item = self.items(event.scenePos())

        if self.image_item in current_item:
            current_item.remove(self.image_item)

        object_items = [
            item
            for item in current_item
            if item.__class__
            in [PolygonAnnotation, PointAnnotation, RectangleAnnotation, PathAnnotation]
        ]

        if object_items:
            item_top: (
                PolygonAnnotation
                | PointAnnotation
                | RectangleAnnotation
                | PathAnnotation
            ) = object_items[0]
            tooltip = None
            if item_top.projection:
                cropped_image = self.db.get_cropped_image(item_top.object_id)
                if cropped_image:
                    if cropped_image["cropped_image"]:
                        tooltip = create_tooltip_cropped_image(
                            cropped_image["cropped_image"],
                            item_top.image_id,
                            item_top.object_type,
                            item_top.resight_set,
                            item_top.source,
                            item_top.reviewed,
                        )
            if not tooltip:
                tooltip = create_tooltip_objects(
                    item_top.image_id,
                    item_top.object_type,
                    item_top.resight_set,
                    item_top.source,
                    item_top.reviewed,
                )
            item_top.setToolTip(tooltip)

        super(ImageScene, self).helpEvent(event)

    def clear_scene(self):

        if self.items():
            self.clear()
            self.working_instruction = False

    def clear(self):
        self.measure_item = None
        self.working_instruction = False
        super(ImageScene, self).clear()

    def set_measure_gsd(self, gsd: float | None):
        self.measure_gsd = gsd if gsd is not None else 0.0

    def set_image_datetime(self, image_datetime):
        self.image_datetime = image_datetime

    def clear_measurement(self):
        if self.measure_item is not None:
            if self.measure_item.scene() is self:
                self.removeItem(self.measure_item)
            self.measure_item = None

    def abort_geometry_operation(self):
        aborted = False

        if self.working_instruction:
            if self.current_instruction in {
                Instructions.Move_Instruction,
                Instructions.Change_Instruction,
                Instructions.Add_Vertex,
            }:
                if self.active_item is not None:
                    self._restore_geometry(self.active_item, self._original_geometry)
                    aborted = True

            elif self.current_instruction == Instructions.Polygon_Instruction:
                if self.polygon_item is not None and self.polygon_item.scene() is self:
                    self.removeItem(self.polygon_item)
                    aborted = True
                if self.p1_poly is not None and self.p1_poly.scene() is self:
                    self.removeItem(self.p1_poly)
                    aborted = True
                self.polygon_item = None
                self.p1_poly = None

            elif self.current_instruction == Instructions.LineString_Instruction:
                if self.path_item is not None and self.path_item.scene() is self:
                    self.removeItem(self.path_item)
                    aborted = True
                self.path_item = None

            elif self.current_instruction == Instructions.Rectangle_Instruction:
                if (
                    self.rectangle_item is not None
                    and self.rectangle_item.scene() is self
                ):
                    self.removeItem(self.rectangle_item)
                    aborted = True
                self.rectangle_item = None

            elif self.current_instruction == Instructions.Measure_Instruction:
                if self.measure_item is not None and self.measure_item.scene() is self:
                    self.removeItem(self.measure_item)
                    aborted = True
                self.measure_item = None

        self.active_item = None
        self.change_point_index = -1
        self.old_coords = None
        self._original_geometry = None
        self.working_instruction = False

        if self.current_instruction != Instructions.No_Instruction:
            aborted = True

        return aborted

    def filter_projection_time(self, max_minutes: int | None):
        current_datetime = self._datetime_from_value(self.image_datetime)

        for item in self.items():
            if not getattr(item, "projection", False):
                continue

            if max_minutes is None:
                item.setVisible(True)
                continue

            item_datetime = self._datetime_from_value(
                getattr(item, "image_datetime", None)
            )
            if current_datetime is None or item_datetime is None:
                item.setVisible(False)
                continue

            delta_minutes = (
                abs((item_datetime - current_datetime).total_seconds()) / 60.0
            )
            item.setVisible(delta_minutes <= max_minutes)

    @staticmethod
    def _datetime_from_value(value):
        if value is None:
            return None

        if isinstance(value, datetime):
            parsed = value
        else:
            try:
                parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
            except ValueError:
                return None

        if parsed.tzinfo is not None:
            parsed = parsed.astimezone(timezone.utc).replace(tzinfo=None)

        return parsed

    # Emit signal to main to store Object into database
    def store_sightings(self, rectangle: QRect, geom_type: str, coords: list):

        if geom_type == "Point":
            points_image = [coords[0].x(), coords[0].y()]
            geom = geometry.Point(points_image)

        elif geom_type == "LineString":
            points_image = list_of_points_to_list(coords)
            geom = geometry.LineString(points_image)

        else:
            points_image = list_of_points_to_list(coords)
            geom = geometry.Polygon(points_image)

        pixmap_bytes = crop_image(self.image_item.pixmap(), rectangle)

        geojson = geometry.mapping(geom)
        obj_id = self.db.create_object(
            self.image_id_db, geojson=geojson, cropped_image=pixmap_bytes
        )
        # tooltip = create_tooltip_objects(self.image_id_db, 'None', 0, reviewed=1, source=0)

        self.element_created.emit(obj_id, geom_type, points_image)

        return obj_id

    def delete_object(self, item_id):
        for item in self.items():
            if hasattr(item, "object_id"):
                if item.object_id == item_id:
                    self.removeItem(item)

    def change_object_type(self, item_list, object_type):
        # self.m_scene2.working_instruction = False
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, "object_id"):
                    if obj.object_id in item_list:
                        obj.object_type = object_type
                        obj.reviewed = 1

    def change_reviewed(self, item_list: list[int]):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, "object_id"):
                    if obj.object_id in item_list:
                        obj.reviewed = 1

    # TODO that functions are same for GIS, could be provided at one module
    def change_resight_set(self, item_list, group_index):
        # self.m_scene2.working_instruction = False
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, "object_id"):
                    if obj.object_id in item_list:
                        obj.resight_set = group_index

    # def change_tooltip(self, item_ids, object_type=None, resight_set=None,
    # None):
    #    for item in self.items():
    #        if hasattr(item, 'object_id'):
    #            if item.object_id in item_ids:
    #                new_html = change_tooltip_html(item.toolTip(), object_type, resight_set, reviewed)
    #                item.setToolTip(new_html)

    def color_objects(
        self,
        attribute: str = None,
        color_dict: dict | None = None,
        default_value=None,
        default_dict: dict | None = None,
    ):

        scene_items = [
            x
            for x in self.items()
            if x.__class__
            in [PolygonAnnotation, PointAnnotation, RectangleAnnotation, PathAnnotation]
        ]
        color_dict_new = None
        if scene_items:
            color_dict_new = color_objects_attribute(
                scene_items,
                attribute,
                color_dict=color_dict,
                default_value=default_value,
                default_dict=default_dict,
            )

        return color_dict_new

    def mouseDoubleClickEvent(self, event):
        if not self.working_instruction and event.button() == Qt.MouseButton.LeftButton:
            current_item = self.items(event.scenePos())
            if self.image_item in current_item:
                current_item.remove(self.image_item)
            object_items = [
                item
                for item in current_item
                if item.__class__
                in [
                    PolygonAnnotation,
                    PointAnnotation,
                    RectangleAnnotation,
                    PathAnnotation,
                ]
            ]
            if object_items:
                self.show_popup.emit(object_items[0].object_id)

    def mousePressEvent(self, event):

        modifiers = QApplication.queryKeyboardModifiers()
        current_item = self.items(event.scenePos())

        if (
            self.working_instruction
            and self.current_instruction
            in {
                Instructions.Move_Instruction,
                Instructions.Change_Instruction,
                Instructions.Add_Vertex,
            }
            and event.button() == Qt.MouseButton.LeftButton
        ):
            self.abort_geometry_operation()
            event.accept()
            return

        if (
            self.working_instruction
            and self.current_instruction
            in {
                Instructions.Move_Instruction,
                Instructions.Change_Instruction,
                Instructions.Add_Vertex,
            }
            and event.button() == Qt.MouseButton.RightButton
        ):
            self._handle_geometry_edit_press(event)
            event.accept()
            return

        if self.image_item in current_item:
            # Remove image form items. Only geometries are left in current items list
            current_item.remove(self.image_item)

            # -----------------------------------------------------------------------------------------------
            # STACK CHANGE
            if (
                len(current_item) > 1
                and not self.working_instruction
                and event.button() == Qt.MouseButton.MiddleButton
            ):
                current_item[0].stackBefore(current_item[-1])

            # -----------------------------------------------------------------------------------------------
            # Group Re-sightings for selected Items by popup Menu
            if (
                self.selectedItems()
                and not self.working_instruction
                and event.button() == Qt.MouseButton.RightButton
                and modifiers == Qt.KeyboardModifier.ControlModifier
            ):
                if len(self.selectedItems()) > 0:
                    self.context_menu = QMenu()

                    if len(self.selectedItems()) > 1:
                        text = "Resight Set"
                        resight_set = self.context_menu.addAction(text)
                        selected_index = [x.object_id for x in self.selectedItems()]
                        resight_set.triggered.connect(
                            lambda: self.resight_set.emit(selected_index, False)
                        )

                    elif len(self.selectedItems()) == 1:
                        text = "Clear Resight Set"
                        group_clear_resight = self.context_menu.addAction(text)
                        selected_index = [x.object_id for x in self.selectedItems()]
                        group_clear_resight.triggered.connect(
                            lambda: self.resight_set.emit(selected_index, True)
                        )

                    delete_objects = self.context_menu.addAction("Delete Selection")
                    delete_objects.triggered.connect(self.delete_selected_objects)

                    global_pos = event.screenPos()
                    self.context_menu.popup(global_pos)

            if self._handle_geometry_edit_press(event):
                event.accept()
                return

            # -----------------------------------------------------------------------------------------------
            # Drawing instructions
            if not self.selectedItems():
                # POINT PICKING
                if (
                    self.current_instruction == Instructions.Point_Instruction
                    and event.button() == Qt.MouseButton.RightButton
                ):
                    point_item = PointAnnotation(
                        color=self.standard_color, image_id=self.image_id_db
                    )
                    point_item.setRect(
                        event.scenePos().x() - point_size / 2.0,
                        event.scenePos().y() - point_size / 2.0,
                        point_size,
                        point_size,
                    )
                    self.working_instruction = False
                    coordinates = [event.scenePos().x(), event.scenePos().y()]
                    point_item.object_id = self.store_sightings(
                        QRect(
                            int(coordinates[0]) - 25, int(coordinates[1]) - 25, 50, 50
                        ),
                        "Point",
                        [event.scenePos()],
                    )
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
                            self.p1_poly.setRect(
                                event.scenePos().x() - point_size / 2.0,
                                event.scenePos().y() - point_size / 2.0,
                                point_size,
                                point_size,
                            )

                            self.polygon_item = PolygonAnnotation(
                                color=self.standard_color, image_id=self.image_id_db
                            )
                            self.addItem(self.polygon_item)
                            self.working_instruction = True
                            self.polygon_item.setPolygon(QPolygonF())
                            poly = self.polygon_item.polygon()
                            poly.append(event.scenePos())
                            self.polygon_item.setPolygon(poly)

                    # Path
                    if self.current_instruction == Instructions.LineString_Instruction:
                        if event.button() == Qt.MouseButton.RightButton:
                            self.path_item = PathAnnotation(
                                color=self.standard_color, image_id=self.image_id_db
                            )
                            self.addItem(self.path_item)

                            path = QPainterPath(event.scenePos())
                            path.lineTo(
                                event.scenePos().x() + 1, event.scenePos().y() + 1
                            )
                            self.path_item.setPath(path)
                            self.working_instruction = True

                    # Measure path
                    if self.current_instruction == Instructions.Measure_Instruction:
                        if (
                            event.button() == Qt.MouseButton.RightButton
                            and self.measure_gsd > 0.0
                        ):
                            self.clear_measurement()
                            self.measure_item = MeasurePathAnnotation(
                                gsd=self.measure_gsd
                            )
                            self.addItem(self.measure_item)

                            path = QPainterPath(event.scenePos())
                            path.lineTo(
                                event.scenePos().x() + 1, event.scenePos().y() + 1
                            )
                            self.measure_item.setPath(path)
                            self.working_instruction = True

                    # Rectangle
                    if self.current_instruction == Instructions.Rectangle_Instruction:
                        if event.button() == Qt.MouseButton.RightButton:
                            self.rectangle_item = RectangleAnnotation(
                                color=self.standard_color, image_id=self.image_id_db
                            )
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
                                rect = (
                                    self.polygon_item.polygon().boundingRect().toRect()
                                )
                                coords = self.polygon_item.polygon().toList()
                                self.polygon_item.object_id = self.store_sightings(
                                    rect, "Polygon", coords
                                )
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
                            self.path_item.object_id = self.store_sightings(
                                rect, "LineString", coords
                            )
                            # self.path_item.setToolTip(tooltip)

                        # Continue Path
                        elif event.button() == Qt.MouseButton.RightButton:
                            path = self.path_item.path()
                            pos_new = event.scenePos()
                            if path.currentPosition() == pos_new:
                                pos_new = pos_new + QPointF(1, 1)
                            path.lineTo(pos_new)
                            self.path_item.setPath(path)

                    if self.current_instruction == Instructions.Measure_Instruction:
                        # Finish measurement
                        if event.button() == Qt.MouseButton.LeftButton:
                            self.working_instruction = False

                        # Continue measurement
                        elif event.button() == Qt.MouseButton.RightButton:
                            path = self.measure_item.path()
                            pos_new = event.scenePos()
                            if path.currentPosition() == pos_new:
                                pos_new = pos_new + QPointF(1, 1)
                            path.lineTo(pos_new)
                            self.measure_item.setPath(path)

                    # Finish Rectangle
                    if self.current_instruction == Instructions.Rectangle_Instruction:
                        # Finish Rectangle
                        if event.button() == Qt.MouseButton.RightButton:
                            self.working_instruction = False
                            rect = self.rectangle_item.rect().toRect()
                            coords = QPolygonF(self.rectangle_item.rect()).toList()
                            self.rectangle_item.object_id = self.store_sightings(
                                rect, "Polygon", coords
                            )
                            # self.rectangle_item.setToolTip(tooltip)
        # -----------------------------------------------------------------------------------------------
        # geometry outside of image due too projection
        else:
            # Stacking of sightings with Middle Button
            if (
                len(current_item) > 1
                and not self.working_instruction
                and event.button() == Qt.MouseButton.MiddleButton
            ):
                current_item[0].stackBefore(current_item[-1])

        # -----------------------------------------------------------------------------------------------
        # Pass Event
        super(ImageScene, self).mousePressEvent(event)

    def _handle_geometry_edit_press(self, event):
        edit_instructions = {
            Instructions.Move_Instruction,
            Instructions.Change_Instruction,
            Instructions.Add_Vertex,
            Instructions.Remove_Vertex,
        }
        if (
            self.current_instruction not in edit_instructions
            or event.button() != Qt.MouseButton.RightButton
        ):
            return False

        if self.current_instruction == Instructions.Move_Instruction:
            if not self.working_instruction:
                item = self._top_selected_editable_item_at(event.scenePos())
                if item is None:
                    return True
                self.active_item = item
                self.old_coords = event.scenePos()
                self._original_geometry = self._capture_geometry(item)
                self.working_instruction = True
            else:
                self._finish_geometry_change()
            return True

        if self.current_instruction == Instructions.Change_Instruction:
            if not self.working_instruction:
                item, idx_point = self._selected_editable_item_close_to_point(
                    event.scenePos()
                )
                if item is None:
                    return True
                self.active_item = item
                self.change_point_index = idx_point
                self._original_geometry = self._capture_geometry(item)
                self.working_instruction = True
            else:
                self._finish_geometry_change()
            return True

        if self.current_instruction == Instructions.Add_Vertex:
            if not self.working_instruction:
                octo = self._octo_at(event.scenePos())
                for item in self._selected_editable_items():
                    if isinstance(item, (PolygonAnnotation, PathAnnotation)):
                        found_near, idx_point, inter_p = item.close_octo(octo)
                        if found_near:
                            self._original_geometry = self._capture_geometry(item)
                            if item.insert_point_after(idx_point, inter_p):
                                self.active_item = item
                                self.change_point_index = idx_point + 1
                                self.working_instruction = True
                            break
            else:
                self._finish_geometry_change()
            return True

        if self.current_instruction == Instructions.Remove_Vertex:
            item, idx_point = self._selected_editable_item_close_to_point(
                event.scenePos(), allowed=(PolygonAnnotation, PathAnnotation)
            )
            if item is not None:
                original_geometry = self._capture_geometry(item)
                if item.remove_point(idx_point):
                    if not self._persist_geometry_change(item):
                        self._restore_geometry(item, original_geometry)
                else:
                    self._restore_geometry(item, original_geometry)
            return True

        return False

    def _finish_geometry_change(self):
        if self.active_item is not None and not self._persist_geometry_change(
            self.active_item
        ):
            self._restore_geometry(self.active_item, self._original_geometry)

        self.active_item = None
        self.change_point_index = -1
        self.old_coords = None
        self._original_geometry = None
        self.working_instruction = False

    def _is_editable_item(self, item):
        return (
            item.__class__
            in [PolygonAnnotation, PointAnnotation, RectangleAnnotation, PathAnnotation]
            and not getattr(item, "projection", False)
            and getattr(item, "source", ObjectSourceList.manual)
            == ObjectSourceList.manual
        )

    def _editable_items(self):
        return [item for item in self.items() if self._is_editable_item(item)]

    def _selected_editable_items(self):
        return [item for item in self.selectedItems() if self._is_editable_item(item)]

    def has_selected_editable_items(self):
        return bool(self._selected_editable_items())

    def _top_selected_editable_item_at(self, pos):
        selected_items = self._selected_editable_items()
        for item in self.items(pos):
            if item in selected_items:
                return item
        return None

    def _selected_editable_item_close_to_point(self, pos, allowed=None):
        if allowed is None:
            allowed = (PolygonAnnotation, RectangleAnnotation, PathAnnotation)

        pick_radius = self._pick_radius()
        for item in self._selected_editable_items():
            if isinstance(item, allowed):
                found_near_geometry, idx_point = item.close_point(pos, pick_radius)
                if found_near_geometry:
                    return item, idx_point

        return None, -1

    def _octo_at(self, pos):
        return OctoLines(pos.x(), pos.y(), self._pick_radius())

    def _pick_radius(self):
        pixmap = self.image_item.pixmap()
        if not pixmap.isNull():
            return (pixmap.width() + pixmap.height()) / 2.0 / 100

        scene_rect = self.sceneRect()
        return (scene_rect.width() + scene_rect.height()) / 2.0 / 100

    @staticmethod
    def _capture_geometry(item):
        if isinstance(item, RectangleAnnotation):
            return item.rect()
        if isinstance(item, PointAnnotation):
            return item.rect()
        if isinstance(item, PolygonAnnotation):
            return QPolygonF(item.polygon())
        if isinstance(item, PathAnnotation):
            return QPainterPath(item.path())
        return None

    @staticmethod
    def _restore_geometry(item, geometry_old):
        if geometry_old is None:
            return
        if isinstance(item, RectangleAnnotation):
            item.setRect(geometry_old)
        elif isinstance(item, PointAnnotation):
            item.setRect(geometry_old)
        elif isinstance(item, PolygonAnnotation):
            item.setPolygon(geometry_old)
        elif isinstance(item, PathAnnotation):
            item.setPath(geometry_old)

    def _persist_geometry_change(self, item):
        if self.db is None or getattr(item, "projection", False):
            return False

        geom_type, points_image, crop_rect, valid = self._geometry_storage_data(item)
        if not valid:
            return False

        if geom_type == "Point":
            geom = geometry.Point(points_image)
        elif geom_type == "LineString":
            geom = geometry.LineString(points_image)
        else:
            geom = geometry.Polygon(points_image)

        cropped_image = crop_image(self.image_item.pixmap(), self._crop_rect(crop_rect))
        self.db.update_object_geometry(
            item.object_id, geometry.mapping(geom), cropped_image
        )
        mapping_points = [points_image] if geom_type == "Point" else points_image
        self.element_changed.emit(item.object_id, geom_type, mapping_points)
        return True

    def _geometry_storage_data(self, item):
        pixmap = self.image_item.pixmap()
        image_width = pixmap.width()
        image_height = pixmap.height()

        if isinstance(item, PointAnnotation):
            points_image, valid = item.get_coords(image_width, image_height)
            crop_rect = QRect(
                int(points_image[0]) - 25, int(points_image[1]) - 25, 50, 50
            )
            return "Point", points_image, crop_rect, valid

        if isinstance(item, PathAnnotation):
            points_image, valid = item.get_coords(image_width, image_height)
            return "LineString", points_image, item.boundingRect().toRect(), valid

        if isinstance(item, (PolygonAnnotation, RectangleAnnotation)):
            points_image, valid = item.get_coords(image_width, image_height)
            return "Polygon", points_image, item.boundingRect().toRect(), valid

        return "", [], QRect(), False

    def _crop_rect(self, rect: QRect):
        pixmap = self.image_item.pixmap()
        left = max(0, rect.left() - 5)
        top = max(0, rect.top() - 5)
        right = min(pixmap.width() - 1, rect.right() + 5)
        bottom = min(pixmap.height() - 1, rect.bottom() + 5)

        if right < left:
            right = left
        if bottom < top:
            bottom = top

        return QRect(left, top, max(1, right - left + 1), max(1, bottom - top + 1))

    def delete_selected_objects(self) -> None:

        v = POPUPConfirm("Are you sure about that operation?")
        if v.exec():
            objects_to_delete = []
            seen_object_ids = set()
            for item in self.selectedItems():
                if not hasattr(item, "object_id") or item.object_id in seen_object_ids:
                    continue
                objects_to_delete.append((item.object_id, item.image_id))
                seen_object_ids.add(item.object_id)

            if not objects_to_delete:
                return

            for obj_id, image_id in objects_to_delete:
                self.object_delete.emit(obj_id, image_id)

    # -----------------------------------------------------------------------------------------------
    # If drawing is active for polygon or rectangle visually show the dynamic outlines
    def mouseMoveEvent(self, event):
        current_item = self.items(event.scenePos())

        if (
            self.current_instruction == Instructions.Change_Instruction
            and self.working_instruction
        ):
            self.active_item.change_geometry(event.scenePos(), self.change_point_index)

        if (
            self.current_instruction == Instructions.Add_Vertex
            and self.working_instruction
        ):
            self.active_item.change_geometry(event.scenePos(), self.change_point_index)

        if (
            self.current_instruction == Instructions.Move_Instruction
            and self.working_instruction
        ):
            change_vector = event.scenePos() - self.old_coords
            self.active_item.move([change_vector.x(), change_vector.y()])
            self.old_coords = event.scenePos()

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
                    path.setElementPositionAt(
                        idx, event.scenePos().x(), event.scenePos().y()
                    )
                    self.path_item.setPath(path)

                if self.current_instruction == Instructions.Measure_Instruction:
                    path = self.measure_item.path()
                    idx = path.elementCount() - 1
                    path.setElementPositionAt(
                        idx, event.scenePos().x(), event.scenePos().y()
                    )
                    self.measure_item.setPath(path)

                # Rectangle
                if self.current_instruction == Instructions.Rectangle_Instruction:
                    self.rectangle_item.resize_rectangle(event.scenePos())

        super(ImageScene, self).mouseMoveEvent(event)
