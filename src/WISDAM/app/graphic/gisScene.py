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


from PySide6.QtWidgets import QGraphicsScene, QApplication, QMenu
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QPainterPath

from app.graphic.itemsGrahpicScene import (PointAnnotation, PolygonAnnotation, RectangleAnnotation,
                                           PolygonFootprint, PathAnnotation, PointCenterpoint, SelectionPolygon)
# from app.utils_qt import change_tooltip_html
from app.graphic.items_coloring import color_objects_attribute
from app.var_classes import Selection
from app.utils_qt import create_tooltip_cropped_image, create_tooltip_objects
from db.dbHandler import DBHandler


class GISScene(QGraphicsScene):
    show_popup = Signal(int)
    resight_set = Signal(list, bool)
    # group_clear_resight = Signal(list)
    group_images = Signal(list)
    goto_image = Signal(int)
    selected_images = Signal(list)
    deselect_images = Signal()
    change_image_meta_list = Signal(list)
    change_image_transect_list = Signal(list)
    change_image_block_list = Signal(list)

    def __init__(self, parent=None):
        super(GISScene, self).__init__(parent)

        self.hide_images_flag = True
        self.show_footprints_on_hover_flag = True

        self.db: DBHandler | None = None

        self.mouse_lef_pressed = False
        self.selection_polygon: SelectionPolygon | None = None
        self.selection_path = QPainterPath()
        self.selection_mode = Selection.Rectangle
        self.context_menu = QMenu()

    def helpEvent(self, event):

        current_item = self.items(event.scenePos())

        if current_item:
            if hasattr(current_item[0], 'object_id'):

                cropped_image = self.db.get_cropped_image(current_item[0].object_id)
                if cropped_image:
                    if cropped_image['cropped_image']:
                        tooltip = create_tooltip_cropped_image(cropped_image['cropped_image'], current_item[0].image_id,
                                                               current_item[0].object_type,
                                                               current_item[0].resight_set, current_item[0].source,
                                                               current_item[0].reviewed)
                    else:
                        tooltip = create_tooltip_objects(current_item[0].image_id,
                                                         current_item[0].object_type,
                                                         current_item[0].resight_set, current_item[0].source,
                                                         current_item[0].reviewed)

                    current_item[0].setToolTip(tooltip)

        super(GISScene, self).helpEvent(event)

    def clear_objects(self):
        for item in self.items():
            if hasattr(item, 'object_id'):
                self.removeItem(item)

    def set_selection_mode(self, selection_mode: Selection):
        self.selection_mode = selection_mode

    def delete_object(self, item_id):
        for item in self.items():
            if hasattr(item, 'object_id'):
                if item.object_id == item_id:
                    self.removeItem(item)

    def show_footprints_on_hover(self, is_checked):
        self.show_footprints_on_hover_flag = is_checked

    def hide_images(self, is_checked):
        scene_items = self.items()
        self.hide_images_flag = is_checked
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PolygonFootprint]:
                    obj.setVisible(not is_checked)

    def hide_centerpoints(self, hide_centerpoints):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PointCenterpoint]:
                    obj.setVisible(not hide_centerpoints)

    def hide_objects(self, button_checked: bool):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PolygonAnnotation, PointAnnotation, RectangleAnnotation, PathAnnotation]:
                    obj.setVisible(not button_checked)

    # def change_tooltip(self, item_ids, object_type: str = None, resight_set: int = None, reviewed=None):
    #    scene_items = self.items()
    #    if scene_items:
    #        for item in scene_items:
    #            if hasattr(item, 'object_id'):
    #                if item.object_id in item_ids:
    #                    new_html = change_tooltip_html(item.toolTip(), object_type, resight_set, reviewed)
    #                    item.setToolTip(new_html)

    def color_objects(self, attribute: str = None, color_dict: dict | None = None,
                      default_value=None, default_dict: dict | None = None):

        scene_items = [x for x in self.items() if x.__class__ in [PolygonAnnotation,
                                                                  PointAnnotation, RectangleAnnotation, PathAnnotation]]
        color_dict_new = None
        if scene_items:
            color_dict_new = color_objects_attribute(scene_items, attribute, color_dict=color_dict,
                                                     default_value=default_value, default_dict=default_dict)

        return color_dict_new

    #def color_single_images(self,image_id: list | int, attribute: str = None, value:object = '',
    #                       color_dict: dict |None=None ):
    #    if not color_dict:
    #      return self.color_images(attribute= attribute, default_value, default_dict)
#
 #       if color_dict.get('attribute')
#
 #       scene_items = [x for x in self.items() if x.__class__ in [PolygonFootprint, PointCenterpoint]]
#
 #       color_dict = None
  #      if scene_items:
   #         color_dict = color_objects_attribute(scene_items, attribute,
    #                                             default_value=default_value, default_dict=default_dict)
#
 #       return color_dict

    def color_images(self, attribute: str = None, default_value=None,
                     default_dict: dict | None = None):
        scene_items = [x for x in self.items() if x.__class__ in [PolygonFootprint, PointCenterpoint]]

        color_dict = None
        if scene_items:
            color_dict = color_objects_attribute(scene_items, attribute,
                                                 default_value=default_value, default_dict=default_dict)

        return color_dict

    def change_survey_data(self, item_list, transect='', flight_ref='', block='', update_all=False):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PolygonFootprint, PointCenterpoint]:
                    if obj.image_id in item_list:
                        if transect or update_all:
                            obj.transect = transect
                        if flight_ref or update_all:
                            obj.flight_ref = flight_ref
                        if block or update_all:
                            obj.block = block

    def change_object_type(self, item_list, object_type):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.object_type = object_type
                        # Set reviewed to one as change_object_type is the only way to review objects
                        obj.reviewed = 1

    def change_resight_set(self, item_list, group_index):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.resight_set = group_index

    def change_reviewed(self, item_list: list[int]):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if hasattr(obj, 'object_id'):
                    if obj.object_id in item_list:
                        obj.reviewed = 1

    def change_image_inspected(self, item_list: list):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PolygonFootprint, PointCenterpoint]:

                    if obj.image_id in item_list:
                        obj.inspected = 1

    def change_image_group(self, item_list, group_index):
        scene_items = self.items()
        if scene_items:
            for obj in scene_items:
                if obj.__class__ in [PolygonFootprint, PointCenterpoint]:

                    if obj.image_id in item_list:
                        obj.group_image = group_index

    def mouseDoubleClickEvent(self, event) -> None:

        if event.modifiers() != Qt.KeyboardModifier.ControlModifier:
            if event.button() == Qt.MouseButton.LeftButton:

                current_item = self.items(event.scenePos())
                current_item = [x for x in current_item if x.__class__ in [RectangleAnnotation, PointAnnotation,
                                                                           PolygonAnnotation, PathAnnotation]]

                if current_item:
                    self.show_popup.emit(current_item[0].object_id)
        super(GISScene, self).mouseDoubleClickEvent(event)

    def mousePressEvent(self, event):

        self.delete_selection_polygon()
        self.mouse_lef_pressed = False

        if event.modifiers() != Qt.KeyboardModifier.ControlModifier:
            self.selection_path = QPainterPath()
            self.setSelectionArea(self.selection_path)

        if event.button() == Qt.MouseButton.LeftButton:
            self.selection_polygon = SelectionPolygon()
            self.addItem(self.selection_polygon)
            self.mouse_lef_pressed = True

        current_item = self.items(event.scenePos())

        current_item = [x for x in current_item if x.__class__ in [RectangleAnnotation, PointAnnotation,
                                                                   PolygonAnnotation, PathAnnotation, PointCenterpoint]]
        if len(current_item) >= 1:

            # STACK CHANGE
            if event.button() == Qt.MouseButton.MiddleButton:
                current_item[0].hoover_active = False
                current_item[0].stackBefore(current_item[-1])

            if (not current_item[0].isSelected()) and (event.button() == Qt.RightButton):
                self.goto_image.emit(current_item[0].image_id)

        modifiers = QApplication.queryKeyboardModifiers()
        # Resight Set
        if self.selectedItems() and modifiers == Qt.KeyboardModifier.ControlModifier \
                and event.button() == Qt.MouseButton.RightButton:
            if len(self.selectedItems()) >= 1:

                current_item_objects = [x.object_id for x in self.selectedItems() if
                                        x.__class__ in [RectangleAnnotation, PointAnnotation,
                                                        PolygonAnnotation, PathAnnotation]]
                current_item_footprint = [x.image_id for x in self.selectedItems() if
                                          x.__class__ in [PointCenterpoint]]
                self.context_menu = QMenu()

                if len(current_item_objects) > 1:
                    text = "Resight Set"
                    resight_set = self.context_menu.addAction(text)
                    resight_set.triggered.connect(lambda: self.resight_set.emit(current_item_objects, False))

                if len(current_item_objects) == 1:
                    text = "Clear Resight Set"
                    group_clear_resight = self.context_menu.addAction(text)
                    group_clear_resight.triggered.connect(lambda: self.resight_set.emit(current_item_objects, True))

                if len(current_item_footprint) > 1:
                    text = "Group Image"
                    group_image = self.context_menu.addAction(text)
                    group_image.triggered.connect(lambda: self.group_images.emit(current_item_footprint))

                if len(current_item_footprint) >= 1:
                    text = "Change Image Meta Data"
                    change_meta = self.context_menu.addAction(text)
                    change_meta.triggered.connect(lambda: self.change_image_meta_list.emit(current_item_footprint))
                    text = "Change Block"
                    change_meta = self.context_menu.addAction(text)
                    change_meta.triggered.connect(lambda: self.change_image_block_list.emit(current_item_footprint))
                    text = "Change Transect"
                    change_meta = self.context_menu.addAction(text)
                    change_meta.triggered.connect(lambda: self.change_image_transect_list.emit(current_item_footprint))

                if len(current_item_footprint) >= 1 or len(current_item_objects) > 0:
                    # self.clearSelection()
                    global_pos = event.screenPos()
                    self.context_menu.popup(global_pos)

        super(GISScene, self).mousePressEvent(event)

    def delete_selection_polygon(self):
        if self.selection_polygon is not None:
            v = QPainterPath()
            v.addPolygon(self.selection_polygon.polygon())
            self.selection_path = self.selection_path.united(v)
            # self.selection_path.addPolygon()
            self.removeItem(self.selection_polygon)
            self.selection_polygon = None

    def mouseReleaseEvent(self, event):

        self.mouse_lef_pressed = False
        # If user is in selection mode current selection will be added to the selection path
        # by union. Otherwise, the sub polygons of the selection path would select/unselect each item
        # by undefined behaviour. Probably by the order polygons are created.
        # print(self.selection_polygon)
        self.delete_selection_polygon()

        # Propagate the selection of footprints to the image pane
        # Quite slow the abstract model
        # if event.button() == Qt.LeftButton:
        #
        #    if self.selectedItems():
        #       selected_footprint_persistent_index = [x.persistent_index for x in self.selectedItems() if
        #                                              x.__class__ == PointCenterpoint]
        #       self.selected_images.emit(selected_footprint_persistent_index)
        #    else:
        #       self.deselect_images.emit()

        super(GISScene, self).mouseReleaseEvent(event)

    def mouseMoveEvent(self, event):

        if self.mouse_lef_pressed:

            if self.selection_polygon is not None:
                if self.selection_mode == Selection.Lasso:
                    poly = self.selection_polygon.polygon()
                    poly.append(event.scenePos())
                    self.selection_polygon.setPolygon(poly)
                    v = QPainterPath()
                    v.addPolygon(poly)
                    united = self.selection_path.united(v)
                    self.setSelectionArea(united, Qt.ItemSelectionOperation.ReplaceSelection)

        super(GISScene, self).mouseMoveEvent(event)
