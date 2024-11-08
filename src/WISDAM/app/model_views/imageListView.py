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


from __future__ import annotations
from enum import IntEnum
from pathlib import Path

from PySide6.QtCore import (Qt, Signal, SignalInstance, QAbstractItemModel, QModelIndex,
                            QItemSelectionModel, QPersistentModelIndex)
from PySide6.QtWidgets import QStyleOptionViewItem, QStyledItemDelegate, QMenu, QTreeView
from PySide6.QtGui import QBrush, QIcon, QMouseEvent

from app.var_classes import image_list_header, ColorGui, ImageList, image_list_folder_dummy
from WISDAMcore.image.base_class import ImageType


class RolesImagePane(IntEnum):
    id = Qt.UserRole + 1


class IconCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(IconCenterDelegate, self).initStyleOption(option, index)
        option.decorationAlignment = (Qt.AlignHCenter | Qt.AlignCenter)
        option.decorationPosition = QStyleOptionViewItem.Top


class ImageTreeView(QTreeView):
    georef_signal: SignalInstance = Signal(list)
    delete_images: SignalInstance = Signal(list)
    delete_folder: SignalInstance = Signal(object)
    change_image_meta_folder: SignalInstance = Signal(object)
    change_image_meta_list: SignalInstance = Signal(list)
    assign_environment: SignalInstance = Signal(int, list, bool)

    def __init__(self, parent=None):
        super(ImageTreeView, self).__init__(parent)
        self.context_menu = QMenu()

    def select_images(self, persistent_index_list):

        # count = 0
        select = QItemSelectionModel()
        select.setModel(self.model())
        # root_childs = self.model().root_item.child_items
        # for idx, parent in enumerate(root_childs):
        #    parent_item = self.model().index(idx, 0)
        #    for idx_child, child in enumerate(parent.child_items):
        #        if child.data(ImageList.id) in image_ids:
        #            child_index = self.model().index(idx_child, 0, parent_item)
        #            select.select(child_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        for p_index in persistent_index_list:
            select.select(p_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        self.setSelectionModel(select)
        # self.selectionModel().select(child_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)

    def mousePressEvent(self, event: QMouseEvent) -> None:

        if event.button() == Qt.RightButton:
            self.context_menu = QMenu()

            index_mouse = self.indexAt(event.position().toPoint())

            if self.model().get_item(index_mouse).child_count() > 1:
                self.clearSelection()
                text = "Delete all data from folder"
                delete_image = self.context_menu.addAction(text)
                path = self.model().get_item(index_mouse).data(ImageList.path)
                delete_image.triggered.connect(lambda: self.delete_folder.emit(path))

                text = "Change metad data"
                change_image = self.context_menu.addAction(text)
                change_image.triggered.connect(lambda: self.change_image_meta_folder.emit(path))

                global_pos = event.screenPos().toPoint()
                self.context_menu.popup(global_pos)
                return

            selected_index_child = [self.model().get_item(x).data(ImageList.id) for x in self.selectedIndexes()
                                    if self.model().get_item(x).child_count() == 0]
            selected_index_child = list(set(selected_index_child))

            if len(selected_index_child) > 0:

                clicked_image_id = self.model().get_item(index_mouse).data(ImageList.id)

                if clicked_image_id in selected_index_child:
                    #text = "Change geo-reference"
                    #georef_action = self.context_menu.addAction(text)
                    #georef_action.triggered.connect(lambda: self.georef_signal.emit(selected_index_child))

                    text = "Delete images"
                    delete_image = self.context_menu.addAction(text)
                    delete_image.triggered.connect(lambda: self.delete_images.emit(selected_index_child))

                    text = "Change image meta data"
                    change_image_meta = self.context_menu.addAction(text)
                    change_image_meta.triggered.connect(lambda:
                                                        self.change_image_meta_list.emit(selected_index_child))

                # Make sure that if only one index is selected, and it's the one to copy from do not show that menu
                if self.model().get_item(index_mouse).child_count() == 0:
                    if not (len(selected_index_child) == 1 and clicked_image_id == selected_index_child[0]):
                        text = "Assign environment to selected images"
                        assign_environment = self.context_menu.addAction(text)
                        assign_environment.triggered.connect(lambda:
                                                             self.assign_environment.emit(clicked_image_id,
                                                                                          selected_index_child,
                                                                                          False))

                        text = "Assign environment to selected images and sightings"
                        assign_environment = self.context_menu.addAction(text)
                        assign_environment.triggered.connect(lambda: self.assign_environment.emit(clicked_image_id,
                                                                                                  selected_index_child,
                                                                                                  True))
                global_pos = event.screenPos().toPoint()
                self.context_menu.popup(global_pos)
                return
        super(ImageTreeView, self).mousePressEvent(event)


class TreeItem:
    def __init__(self, data: list, parent: TreeItem = None):
        self.item_data = data
        self.parent_item = parent
        self.child_items = []

    def child(self, number: int) -> TreeItem | None:
        if number < 0 or number >= len(self.child_items):
            return None
        return self.child_items[number]

    def last_child(self):
        return self.child_items[-1] if self.child_items else None

    def child_count(self) -> int:
        return len(self.child_items)

    def child_number(self) -> int:
        if self.parent_item:
            return self.parent_item.child_items.index(self)
        return 0

    def column_count(self) -> int:
        return len(self.item_data)

    def data(self, column: int):
        if column < 0 or column >= len(self.item_data):
            return None
        return self.item_data[column]

    def insert_children(self, position: int, count: int, data: list) -> bool:
        if position < 0 or position > len(self.child_items):
            return False

        for row in range(count):
            item = TreeItem(data.copy(), self)
            self.child_items.insert(position, item)

        return True

    def parent(self):
        return self.parent_item

    def remove_children(self, position: int, count: int) -> bool:
        if position < 0 or position + count > len(self.child_items):
            return False

        for row in range(count):
            self.child_items.pop(position)

        return True

    def set_data(self, column: int, value):
        if column < 0 or column >= len(self.item_data):
            return False

        self.item_data[column] = value
        return True


class ImageListModel(QAbstractItemModel):

    def __init__(self, headers: list):
        super(ImageListModel, self).__init__()

        self.root_data = headers
        self.root_item = TreeItem(self.root_data.copy())
        self.flat_tick = QIcon(u":icons/icons/flat_tick_icon.svg")
        self.flat_cross = QIcon(u":icons/icons/flat_cross_icon.svg")
        self.flat_tick_yellow = QIcon(u":icons/icons/flat_tick_icon_yellow.svg")

    def columnCount(self, parent: QModelIndex = None) -> int:
        return self.root_item.column_count()

    def data(self, index: QModelIndex, role: int = None):

        if not index.isValid():
            return None
        item: TreeItem = self.get_item(index)

        # Treat folders differently
        if item.child_count() > 0:
            if role == Qt.DisplayRole:
                # See below for the nested-list data structure.
                # .row() indexes into the outer list,
                # .column() indexes into the sub-list
                if index.column() == ImageList.name:
                    return item.data(index.column())

            # Show path of folder as tooltip
            if role == Qt.ToolTipRole:
                return item.data(ImageList.path).as_posix()

        else:

            if role == Qt.DisplayRole:
                # See below for the nested-list data structure.
                # .row() indexes into the outer list,
                # .column() indexes into the sub-list
                if index.column() not in [ImageList.georef, ImageList.inspected]:
                    return item.data(index.column())

            if role == Qt.TextAlignmentRole:
                if index.column() in [ImageList.georef, ImageList.inspected, ImageList.nr_sightings,
                                      ImageList.gsd, ImageList.area, ImageList.importers, ImageList.ortho]:
                    return Qt.AlignCenter

            if role == RolesImagePane.id:
                return item.data(ImageList.id)

            if role == Qt.BackgroundRole:
                value = item.data(index.column())
                active = item.data(ImageList.active)

                if active:
                    return ColorGui.brush_dark_green

                # ortho indication field
                if index.column() == ImageList.ortho:
                    if value == 'ortho':
                        return QBrush(ColorGui.color_ortho)

                if index.column() == ImageList.name:
                    if not item.data(ImageList.path_exists):
                        return ColorGui.color_no_path

            if role == Qt.DecorationRole:
                value = item.data(index.column())
                if index.column() == ImageList.georef:
                    # if isinstance(value, bool):
                    if value:
                        return self.flat_tick
                    else:
                        return self.flat_cross
                if index.column() == ImageList.inspected:
                    # if isinstance(value, bool):
                    if value > 0:
                        return self.flat_tick_yellow

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        return Qt.ItemIsEditable | QAbstractItemModel.flags(self, index)

    def get_item(self, index: QModelIndex = QModelIndex()) -> TreeItem:
        if index.isValid():
            item: TreeItem = index.internalPointer()
            if item:
                return item

        return self.root_item

    def headerData(self, section: int, orientation: Qt.Orientation,
                   role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self.root_item.data(section)

        return None

    def index(self, row: int, column: int, parent: QModelIndex = QModelIndex()) -> QModelIndex:
        if parent.isValid() and parent.column() != 0:
            return QModelIndex()

        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return QModelIndex()

        child_item: TreeItem = parent_item.child(row)
        if child_item:
            return self.createIndex(row, column, child_item)
        return QModelIndex()

    def insertRows(self, position: int, rows: int,
                   data: list, parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginInsertRows(parent, position, position + rows - 1)
        success: bool = parent_item.insert_children(position, rows, data)
        self.endInsertRows()

        return success

    def parent(self, index: QModelIndex = QModelIndex()) -> QModelIndex:
        if not index.isValid():
            return QModelIndex()

        child_item: TreeItem = self.get_item(index)
        if child_item:
            parent_item: TreeItem | None = child_item.parent()
        else:
            parent_item = None

        if parent_item == self.root_item or not parent_item:
            return QModelIndex()

        return self.createIndex(parent_item.child_number(), 0, parent_item)

    def removeRows(self, position: int, rows: int,
                   parent: QModelIndex = QModelIndex()) -> bool:
        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return False

        self.beginRemoveRows(parent, position, position + rows - 1)
        success: bool = parent_item.remove_children(position, rows)
        self.endRemoveRows()

        return success

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        if parent.isValid() and parent.column() > 0:
            return 0

        parent_item: TreeItem = self.get_item(parent)
        if not parent_item:
            return 0
        return parent_item.child_count()

    #def setData(self, index: QModelIndex| QPersistentModelIndex, value,
    #            role: int = ...) -> bool:
    def setData(self, index: QModelIndex, column: int, value) -> bool:

        item: TreeItem = self.get_item(index)
        result: bool = item.set_data(column, value)

        if result:
            self.dataChanged.emit(QModelIndex(), QModelIndex())#index, index)

        #self.layoutChanged.emit()
        return result

    def add_object(self, index):
        item: TreeItem = self.get_item(index)
        self.setData(index, ImageList.nr_sightings, item.data(ImageList.nr_sightings) + 1)

    def remove_object(self, index):
        item: TreeItem = self.get_item(index)
        self.setData(index, ImageList.nr_sightings, item.data(ImageList.nr_sightings) - 1)

    def setHeaderData(self, section: int, orientation: Qt.Orientation, value,
                      role: int = None) -> bool:
        if role != Qt.EditRole or orientation != Qt.Horizontal:
            return False

        result: bool = self.root_item.set_data(section, value)

        if result:
            self.headerDataChanged.emit(orientation, section, section)

        return result

    def select_images(self, persistent_index_list):
        select = QItemSelectionModel()
        select.setModel(self)
        for p_index in persistent_index_list:
            select.select(p_index, QItemSelectionModel.Select | QItemSelectionModel.Rows)
        return select

    def image_count(self):
        count = 0
        root_childs = self.root_item.child_items
        for child in root_childs:
            count += child.child_count()
        return count

    def image_gsd(self):
        gsd = []
        root_childs = self.root_item.child_items
        for child in root_childs:
            gsd += [float(x.data(ImageList.gsd)) for x in child.child_items if x.data(ImageList.gsd) > 0.0]
        return gsd

    def nr_images_georef(self):
        nr_georef = 0
        root_childs = self.root_item.child_items
        for child in root_childs:
            nr_georef += len([1 for x in child.child_items if x.data(ImageList.gsd) > 0.0])
        return nr_georef

    def nr_images_missing(self):
        root_childs = self.root_item.child_items
        for child in root_childs:
            for x in child.child_items:
                if not x.data(ImageList.path_exists):
                    return True
        return False

    def nr_images_inspected(self):
        inpsected = 0
        root_childs = self.root_item.child_items
        for child in root_childs:
            inpsected += len([1 for x in child.child_items if x.data(ImageList.inspected)])
        return inpsected

    def image_importers(self):
        importers = []
        root_childs = self.root_item.child_items
        for child in root_childs:
            importers += [x.data(ImageList.importers) for x in child.child_items]
        return importers

    def image_folders(self, index=...):
        folder = []
        root_childs = self.root_item.child_items
        for child in root_childs:
            folder += [Path(x.data(ImageList.path)).parent.as_posix() for x in child.child_items]
        return folder

    def change_value(self, index, value):

        item: TreeItem = self.get_item(index)
        item.set_data(index.column(), value)
        #self.layoutChanged.emit()

    def next_index(self, index: QModelIndex):
        parent = index.parent()
        row = index.row() + 1

        if row == self.rowCount(parent):
            # End of rows reached
            row_parent = parent.row() + 1
            if self.root_item.child_count() > row_parent:
                parent = self.index(row_parent, 0, QModelIndex())
                return self.index(0, 0, parent)
        else:
            return self.index(row, 0, parent)

        return QModelIndex()

    def previous_index(self, index: QModelIndex):
        parent = index.parent()
        row = index.row() - 1

        if row < 0:
            # End of rows reached
            if parent.row() > 0:
                parent_index = self.index(parent.row() - 1, 0, QModelIndex())
                last_item = self.get_item(parent_index).child_count() - 1
                return self.index(last_item, 0, parent_index)
        else:
            return self.index(row, 0, parent)

        return QModelIndex()


def digitizer_image_panel_assign_model(data) -> tuple[ImageListModel, dict]:
    list_folder: list[Path] = []
    list_persistent_index_image = {}

    for x in data:
        pt = Path(x['path'])
        if pt.parent not in list_folder:
            list_folder.append(pt.parent)

    list_children = [[] for _ in list_folder]
    for x in data:
        pt = Path(x['path'])
        folder_index = list_folder.index(pt.parent)
        list_children[folder_index].append(x)

    model = ImageListModel(image_list_header)

    # for ch in data:

    parent: TreeItem = model.root_item

    for folder in list_children:

        data_folder = image_list_folder_dummy
        pt = Path(folder[0]['path'])
        data_folder[ImageList.name] = pt.parent.name
        data_folder[ImageList.path] = pt.parent
        parent.insert_children(parent.child_count(), 1, data_folder)
        parent_child: TreeItem = parent.last_child()
        parent_item = model.index(parent.child_count() - 1, 0)

        for rows in folder:

            georef = False
            if rows['geom']:
                georef = True

            type_image = ImageType(rows['type']).fullname

            path = Path(rows['path'])
            a = [path.name, rows['id'], rows['inspected'], rows['s_count'],
                 georef, type_image, rows['importer'], rows['gsd'] * 100, rows['area'], rows['path'], False,
                 path.exists()]

            success = parent_child.insert_children(parent_child.child_count(), 1, a)

            if success:
                child_index = model.index(parent_child.child_count()-1, 0, parent_item)
                list_persistent_index_image[path.as_posix()] = QPersistentModelIndex(child_index)

    return model, list_persistent_index_image
