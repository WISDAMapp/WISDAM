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


from pathlib import Path
import logging

from PySide6 import QtCore
from PySide6.QtWidgets import QGraphicsDropShadowEffect, QWidget, QFileDialog
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor

from app.gui_design.ui_path import Ui_popup_path
from app.var_classes import ColorGui

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


class CustomNode(object):
    def __init__(self, data):
        self._data = data
        if type(data) is tuple:
            self._data = list(data)
        if type(data) is str or not hasattr(data, '__getitem__'):
            self._data = [data]

        self._column_count = len(self._data)
        self._children = []
        self._parent = None
        self._row = 0

    def data(self, column):
        if 0 <= column < len(self._data):
            return self._data[column]

    def column_count(self):
        return self._column_count

    def child_count(self):
        return len(self._children)

    def child(self, row):
        if 0 <= row < self.child_count():
            return self._children[row]

    def parent(self):
        return self._parent

    def row(self):
        return self._row

    def add_child(self, child):
        child._parent = self
        child._row = len(self._children)
        self._children.append(child)
        self._column_count = max(child.column_count(), self._column_count)


class CustomModel(QtCore.QAbstractItemModel):
    def __init__(self, nodes):
        QtCore.QAbstractItemModel.__init__(self)
        self._root = CustomNode(None)
        for node in nodes:
            self._root.add_child(node)

    def rowCount(self, index=...):
        if index.isValid():
            return index.internalPointer().child_count()
        return self._root.child_count()

    def add_child(self, node, _parent):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()
        parent.addChild(node)

    def index(self, row, column, _parent=None):
        if not _parent or not _parent.isValid():
            parent = self._root
        else:
            parent = _parent.internalPointer()

        if not QtCore.QAbstractItemModel.hasIndex(self, row, column, _parent):
            return QtCore.QModelIndex()

        child = parent.child(row)
        if child:
            return QtCore.QAbstractItemModel.createIndex(self, row, column, child)
        else:
            return QtCore.QModelIndex()

    def parent(self, index=...):
        if index.isValid():
            p = index.internalPointer().parent()
            if p:
                return QtCore.QAbstractItemModel.createIndex(self, p.row(), 0, p)
        return QtCore.QModelIndex()

    def columnCount(self, index=...):
        if index.isValid():
            return index.internalPointer().column_count()
        return self._root.column_count()

    def data(self, index, role: int = ...):
        if not index.isValid():
            return None
        node = index.internalPointer()
        if role == Qt.ItemDataRole.DisplayRole:
            return node.data(index.column())
        if role == Qt.ItemDataRole.BackgroundRole:

            if index.parent().data():
                path_test = Path(index.parent().data()) / Path(index.data())
            else:
                path_test = Path(index.data())
            if not path_test.exists():
                return ColorGui.color_no_path
            else:
                return ColorGui.brush_dark_green
        return None


class POPUPPathChange(QWidget):
    windowClosed = QtCore.Signal(bool)

    def __init__(self):
        QWidget.__init__(self)

        self.ui = Ui_popup_path()
        self.ui.setupUi(self)
        self.db: DBHandler | None = None
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(17)
        shadow.setXOffset(0)
        shadow.setYOffset(0)
        shadow.setColor(QColor(0, 0, 0, 150))
        self.ui.frame_main.setGraphicsEffect(shadow)

        self.ui.btn_close.clicked.connect(self.close)
        self.ui.treeView_paths.doubleClicked.connect(self.tree_view_double_click)

        self.items = []
        self.roots = []
        self.dragPos: QtCore.QPointF = QtCore.QPointF(0.0, 0.0)
        self.changed = False

        # --------------------------------------------------------------
        # MOVE WINDOW / MAXIMIZE / RESTORE
        def move_window(event):
            if event.buttons() == Qt.MouseButton.LeftButton and not self.isMaximized():
                self.move(self.pos() + event.globalPosition().toPoint() - self.dragPos.toPoint())
                self.dragPos = event.globalPosition()
                event.accept()

        # WIDGET TO MOVE
        self.ui.frame_top.mouseMoveEvent = move_window

        # Close event resets the variable which contains the ID

    def closeEvent(self, event):
        self.windowClosed.emit(self.changed)

    def mousePressEvent(self, event):
        self.dragPos = event.globalPosition()

    def set_db(self, db: DBHandler):
        self.db: DBHandler = db
        self.changed = False

    def get_values(self):

        self.ui.treeView_paths.collapseAll()

        images = self.db.load_images_list()

        # build_tree(data,parent=self.ui1.treeView)
        self.items = []
        self.roots = []

        for rows in images:
            file = Path(rows['path'])

            if file.parent in self.roots:
                root_index = self.roots.index(file.parent)

            else:
                self.items.append(CustomNode(file.parent.as_posix()))
                self.roots.append(file.parent)
                root_index = -1

            self.items[root_index].add_child(CustomNode([file.stem + file.suffix]))

        self.ui.treeView_paths.setModel(CustomModel(self.items))
        self.ui.treeView_paths.collapseAll()

    def tree_view_double_click(self, index):
        # path_previous = index.model().index(self.current_index_image_view, 4).data()
        # georef_flag_previous = index.model().index(self.current_index_image_view, 3).data()

        if index.parent().data():
            ext_data_img_folder = QFileDialog.getExistingDirectory(self, caption="Choose Folder of images")
            if ext_data_img_folder:
                ext_data_img_folder = Path(ext_data_img_folder)
                self.db.update_path(index.parent().data(), ext_data_img_folder.as_posix())
                self.get_values()
                self.changed = True
