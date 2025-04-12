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


from pathlib import Path
import json

from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Signal,
    QSizeF,
    QSize,
    QRect,
    QRectF,
    QPoint,
    QItemSelectionModel,
    Slot,
    QSortFilterProxyModel,
    QPersistentModelIndex,
    SignalInstance,
    QPointF,
    Qt
)

from PySide6.QtWidgets import (
    QListView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QApplication,
    QStyle,
    QMenu,
    QAbstractItemView,
    QFrame)
from PySide6.QtGui import (
    QPainter,
    QFontMetricsF,
    QMouseEvent,
    QFont,
    QPainterPath,
    QIcon,
    QKeyEvent,
    QPen,
    QPixmap, QColor)

from db.dbHandler import DBHandler
from app.var_classes import (GalleryData, ColorGui, GalleryRoles, icon_margin, spacing_grid,
                             text_margin, source_switch, icon_footer_padding, GalleryIconSize)
from app.popups.popupConfirm import POPUPConfirm
from WISDAMcore.image.base_class import ImageType


class GalleryListModel(QAbstractListModel):
    def __init__(self, data):
        super(GalleryListModel, self).__init__()
        self._data = data

        # self.rows = self._data

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.NoItemFlags

        row = index.row()
        if row >= len(self._data) or row < 0:
            return Qt.NoItemFlags

        return super().flags(index) | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def append_data(self, data: GalleryData):
        self.layoutAboutToBeChanged.emit()
        self._data.append(data)
        self.layoutChanged.emit()

    def row(self, row: int):
        """
        get row
        """
        return self._data[row]

    def get_data(self) -> list[GalleryData]:
        return self._data

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row_id = index.row()
        if row_id >= len(self._data) or row_id < 0:
            return None

        row = self._data[row_id]
        if role == GalleryRoles.thumbnail:
            return row.thumbnail
        elif role == GalleryRoles.id:
            return row.id
        elif role == GalleryRoles.type:
            return row.type
        elif role == GalleryRoles.object_type:
            return row.object_type
        elif role == GalleryRoles.source:
            return row.source
        elif role == GalleryRoles.image:
            return row.image
        elif role == GalleryRoles.image_type:
            return row.image_type
        elif role == GalleryRoles.extension:
            return row.extension

        elif role == GalleryRoles.folder:
            return row.folder
        elif role == GalleryRoles.filename:
            return row.filename
        elif role == GalleryRoles.group_area:
            return row.group_area
        elif role == GalleryRoles.resight_set:
            return row.resight_set
        elif role == GalleryRoles.active:
            return row.active
        elif role == GalleryRoles.tags:
            return row.tags
        elif role == GalleryRoles.highlighted:
            return row.highlighted
        elif role == GalleryRoles.reviewed:
            return row.reviewed

    def change_value(self, index: QModelIndex, value):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        if row >= len(self._data) or row < 0:
            self.layoutChanged.emit()
            return False
        self._data[index.row()][index.column()] = value
        self.layoutChanged.emit()
        return True

    def set_resight_set(self, row, value):
        self.layoutAboutToBeChanged.emit()
        self._data[row].resight_set = value
        self.layoutChanged.emit()
        return True

    def set_active(self, index: QModelIndex, value):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        self._data[row].active = value
        self.layoutChanged.emit()
        return True

    def set_highlighted(self, index: QModelIndex, value):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        self._data[row].highlighted = value
        self.layoutChanged.emit()
        return True

    def change_object_tag_reviewed(self, index: QModelIndex, data: GalleryData):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        self._data[row].tags = data.tags
        self._data[row].object_type = data.object_type
        self._data[row].reviewed = 1
        self.layoutChanged.emit()

        return True

    def remove_row_sight_id(self, sight_id, model_index=QModelIndex()):
        """
        Removes Python list rows only, i.e. self.rows.

        Does not touch database or other variables.
        """

        self.layoutAboutToBeChanged.emit()
        position = None
        for idx, row in enumerate(self._data):
            if row.id == sight_id:
                position = idx
                break

        if position is not None:
            self.beginRemoveRows(model_index, position, position)
            del (self._data[position])
            self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    def removeRows(self, position, rows=1, model_index=QModelIndex()):
        """
        Removes Python list rows only, i.e. self.rows.

        Does not touch database or other variables.
        """
        self.layoutAboutToBeChanged.emit()
        self.beginRemoveRows(model_index, position, position + rows - 1)
        for i in range(rows):
            del (self._data[position])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True


class SelectionModel(QItemSelectionModel):
    def __init__(self, parent=None):
        super().__init__(parent)


class GalleryView(QListView):
    """
    Gallery view which shows the objects. QListView in icon mode.
    """
    goto_image: SignalInstance = Signal(int)
    object_delete: SignalInstance = Signal(int, int)
    open_meta: SignalInstance = Signal(int)
    resight_set: SignalInstance = Signal(list, bool)

    # verticalScrollBarVisible = pyqtSignal(bool)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setSpacing(spacing_grid)
        self.setIconSize(QSize(GalleryIconSize.width, GalleryIconSize.height))
        # self.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.setFrameShadow(QFrame.Shadow.Plain)
        # self.clickedIndex = 0
        self.fast_activate = False
        # self.setSelectionModel(SelectionModel())
        # self.selection = self.selectionModel()
        self.selection = False
        self.selected_index = []
        self.clickedIndex = QPersistentModelIndex()
        self.possiblyPreserveSelectionPostClick = False
        self.context_menu = QMenu()
        #self.setMouseTracking(False)

        # Track how many columns the user sees
        # QListView IconMode indexes are always set to column 0
        self.user_visible_columns = 0
        self._db: DBHandler | None = None

    def set_db(self, db: DBHandler):
        self._db = db

    def enterEvent(self, event) -> None:

        pass

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        """
        Change active status.

        :param event: the mouse doubleclick event
        """
        index = self.indexAt(event.position().toPoint())
        if index.isValid():
            self.clickedIndex = QPersistentModelIndex(index)
            obj_id = index.data(GalleryRoles.id)
            if event.button() == Qt.LeftButton:
                self.open_meta.emit(obj_id)

    def mousePressEvent(self, event):
        """
        Change content menu, star, active,....

        :param event: the mouse click event
        """

        if self.model() is not None:

            index = self.indexAt(event.position().toPoint())
            # return
            self.clickedIndex = QPersistentModelIndex(index)
            modifiers = QApplication.queryKeyboardModifiers()

            if self.clickedIndex.isValid():

                if event.button() == Qt.LeftButton:

                    if self.fast_activate and not self.selection:
                        self.activate()
                    if not modifiers == Qt.ControlModifier:
                        self.deselect()

                if event.button() == Qt.RightButton:

                    if self.clickedIndex.isValid():
                        self.context_menu = QMenu()
                        # self.contextMenu.addAction()

                        if self.selection:

                            if not self.fast_activate:

                                self.selected_index = [QPersistentModelIndex(x.model().mapToSource(x))
                                                       for x in self.selectedIndexes()]

                                if len(self.selected_index) > 1:
                                    text = "Resight Set"
                                    context_resight_set = self.context_menu.addAction(text)
                                    context_resight_set.triggered.connect(lambda:
                                                                            self.assign_resight(clear_group=False))
                                else:
                                    text = "Clear Resight Set"
                                    context_group_clear_resight = self.context_menu.addAction(text)
                                    context_group_clear_resight.triggered.connect(
                                        lambda: self.assign_resight(clear_group=True))

                        else:
                            if self.clickedIndex.isValid():
                                if not self.fast_activate:
                                    text = "Activate" if not self.clickedIndex.data(GalleryRoles.active) else "Deactivate"
                                    activate_act = self.context_menu.addAction(text)
                                    activate_act.triggered.connect(self.activate)

                                text = "Highlight Object" if not self.clickedIndex.data(
                                    GalleryRoles.highlighted) else "Un highlight Object"
                                star_image_act = self.context_menu.addAction(text)
                                goto_image_act = self.context_menu.addAction("Go To Image")
                                self.context_menu.addSeparator()
                                copy_path_act = self.context_menu.addAction("Copy Path of image")
                                self.context_menu.addSeparator()
                                delete_act = self.context_menu.addAction("Delete")
                                star_image_act.triggered.connect(self.highlight_action)
                                goto_image_act.triggered.connect(self.goto_image_action)
                                copy_path_act.triggered.connect(self.copy_path_action)
                                delete_act.triggered.connect(self.delete)

                        self.context_menu.popup(self.mapToGlobal(event.position().toPoint()))

            else:
                self.deselect()
        super().mousePressEvent(event)

    def keyReleaseEvent(self, event: QKeyEvent):
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.clearSelection()
        if self.model() is not None:
            self.model().sourceModel().dataChanged.emit(0, 0)
        self.selection = False
        super().keyReleaseEvent(event)

    def deselect(self):
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.clearSelection()
        self.model().sourceModel().dataChanged.emit(0, 0)
        self.selection = False

    def keyPressEvent(self, event: QKeyEvent):
        if event.key() == Qt.Key_Control and not self.fast_activate:
            self.setSelectionMode(QAbstractItemView.SelectionMode.MultiSelection)
            self.selection = True
        super().keyPressEvent(event)

    @Slot()
    def assign_resight(self, clear_group=False):
        # group_index = self._db.db_get_next_resight_set()+1
        # if not group_index:
        #    pass
        item_list = []
        if len(self.selected_index) >= 1:
            for item in self.selected_index:
                if item.isValid():
                    # item.model().set_resight_set(item.row(), group_index)
                    item_list.append(item.data(GalleryRoles.id))

            if item_list:
                item_list = tuple(item_list)
                # self._db.db_set_resight_set(item_list, group_index)
                # self._db.db_set_resight_data(item_list)
                self.resight_set.emit(item_list, clear_group)

    @Slot()
    def activate(self):
        index = self.clickedIndex
        if index.isValid():
            index_model = index.model().mapToSource(index)
            active = 0 if index_model.data(GalleryRoles.active) else 1
            index.model().sourceModel().set_active(index_model, 0 if index_model.data(GalleryRoles.active) else 1)
            self._db.set_active(active, index_model.data(GalleryRoles.id))

    @Slot()
    def highlight_action(self) -> None:
        index = self.clickedIndex
        if index.isValid():
            highlighted = 0 if index.data(GalleryRoles.highlighted) else 1
            index_model = index.model().mapToSource(index)
            index.model().sourceModel().set_highlighted(index_model,
                                                        0 if index_model.data(GalleryRoles.highlighted) else 1)
            self._db.set_highlighted(highlighted, index_model.data(GalleryRoles.id))

    @Slot()
    def copy_path_action(self) -> None:
        index = self.clickedIndex
        if index.isValid():
            index_model = index.model().mapToSource(index)
            path = index_model.data(GalleryRoles.folder)
            QApplication.clipboard().setText(path)

    @Slot()
    def goto_image_action(self):
        index = self.clickedIndex
        if index.isValid():
            index_model = index.model().mapToSource(index)
            image_id = index_model.data(GalleryRoles.image)
            self.goto_image.emit(image_id)

    @Slot()
    def delete(self) -> None:

        v = POPUPConfirm("Are you sure about that operation?")
        if v.exec():

            index = self.clickedIndex
            if index.isValid():
                index_model = index.model().mapToSource(index)
                self.object_delete.emit(index_model.data(GalleryRoles.id),
                                        index_model.data(GalleryRoles.image))
            self.clickedIndex = QPersistentModelIndex()

    def top_left(self):
        return QPoint(icon_margin, icon_margin)

    def thumbnail_width(self) -> int:
        return self.itemDelegate().fixedSizeHint.width()

    def width_required(self, no_thumbnails: int) -> int:
        return (
                no_thumbnails * (self.thumbnail_width() + self.spacing())
                + self.spacing()
                + self.frameWidth() * 2
        )

    def resizeEvent(self, event) -> None:
        """
        Resize, then calculate and store how many columns the user sees
        """
        super().resizeEvent(event)


class GalleryIconDelegate(QStyledItemDelegate):
    """
    Render gallery icons
    """

    def __init__(self, parent=None, thumb_size=GalleryIconSize, db: DBHandler | None = None) -> None:
        super().__init__(parent)

        size24 = QSize(30, 30)

        self.db=db

        star_icon = QIcon(u":/icons/icons/starred.svg")
        self.icon_starred = star_icon.pixmap(size24)

        self.image_width = thumb_size.width
        self.image_height = thumb_size.height
        self.horizontal_margin = float(icon_margin)
        self.vertical_margin = float(icon_margin)

        # self.shadow_size = 2.0
        self.width = self.image_width + self.horizontal_margin * 2
        self.height = (
                self.image_height
                + self.vertical_margin * 2
        )

        font_factor = thumb_size.width / GalleryIconSize.width
        self.emblemFont = QFont()
        self.emblemFont.setPointSize(int(self.emblemFont.pointSize() * font_factor)+2)
        self.emblemFont.setBold(True)
        self.metrics = QFontMetricsF(self.emblemFont)

        # Determine the actual height of the font
        ext = "aaaa".upper()
        tbr = self.metrics.tightBoundingRect(ext)  # type QRectF
        # height = tbr.height()
        self.emblem_height = tbr.height() * 2

        # Size is always fixed, so calculate it here
        self.fixedSizeHint = QSizeF(self.width, self.height).toSize()

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        if index is None:
            return

        if not index.isValid():
            return

        # Save state of painter, restore on function exit
        painter.save()
        painter.eraseRect(option.rect)

        painter.setRenderHint(QPainter.Antialiasing, True)

        obj_id = index.data(GalleryRoles.id)
        active = index.data(GalleryRoles.active)
        image_type = index.data(GalleryRoles.image_type)
        source = index.data(GalleryRoles.source)
        extension = index.data(GalleryRoles.extension)
        object_type = index.data(GalleryRoles.object_type)
        group_area = index.data(GalleryRoles.group_area)
        resight_set = index.data(GalleryRoles.resight_set)
        thumbnail = index.data(GalleryRoles.thumbnail)
        highlighted = index.data(GalleryRoles.highlighted)
        reviewed = index.data(GalleryRoles.reviewed)

        is_selected = option.state & QStyle.StateFlag.State_Selected

        x = option.rect.x()
        y = option.rect.y()

        if active:
            painter.setPen(QPen(ColorGui.color_active, 3))

        else:
            painter.setPen(QPen(ColorGui.color_not_active, 3))

        if is_selected:
            painter.setPen(QPen(ColorGui.color_selection, 3))

        box_rect = QRectF(x + 1.5, y + 1.5, self.width - 3, self.height - 3)
        painter.drawRect(box_rect)

        thumbnail_x = (self.horizontal_margin + x)
        thumbnail_y = (self.vertical_margin + y)

        # Draw pixmap of item
        target = QRectF(thumbnail_x, thumbnail_y, self.width - self.horizontal_margin * 2,
                        self.height - self.vertical_margin * 2)

        # size = thumbnail.size().scaled(target.width(), target.height(), Qt.KeepAspectRatio)
        # painter.drawPixmap(target.x(), target.y(), size.width(), size.height(), thumbnail)
        if thumbnail is None and self.db is not None:
            thumbnail_db = self.db.get_cropped_image(obj_id)
            if thumbnail_db:
                thumbnail = QPixmap()
                thumbnail.loadFromData(thumbnail_db['cropped_image'], "JPG")
        if thumbnail is not None:
            size = thumbnail.size().scaled(target.width(), target.height(), Qt.KeepAspectRatio)
            painter.drawPixmap(target.x(), target.y(), size.width(), size.height(), thumbnail)

        # Draw highlighted icon
        if highlighted:
            star_x = x + self.width - self.icon_starred.width()
            painter.drawPixmap(QPointF(star_x, y), self.icon_starred)

        # Drawing Text Boxes
        painter.setFont(self.emblemFont)

        # Draw a small coloured box containing the file extension in the
        # bottom right corner is the image extension
        extension = extension.upper()
        # Calculate size of extension text
        tbr = self.metrics.tightBoundingRect(extension)  # type: QRectF
        emblem_width = tbr.width() + text_margin * 2
        emblem_rect_x = self.width - self.horizontal_margin - emblem_width + x
        emblem_rect_y = y + self.image_height - self.emblem_height
        emblem_rect = QRectF(emblem_rect_x, emblem_rect_y, emblem_width, self.emblem_height)  # type: QRectF
        color = ColorGui.color_extension
        path = QPainterPath()
        path.addRoundedRect(emblem_rect, 5, 5)
        painter.fillPath(path, color)
        painter.setPen(QColor(Qt.white))
        painter.drawText(emblem_rect, Qt.AlignCenter, extension)

        sec_rect_x = emblem_rect_x
        # Orthophoto or Normal Photo right to the Extension
        tbr = self.metrics.tightBoundingRect(image_type)  # type QRectF
        sec_width = tbr.width() + text_margin * 2
        sec_rect_x = sec_rect_x - (10 + sec_width)
        color = ColorGui.color_ortho
        sec_rect = QRectF(sec_rect_x, emblem_rect_y, sec_width, self.emblem_height)
        path = QPainterPath()
        path.addRoundedRect(sec_rect, 5, 5)
        painter.fillPath(path, color)
        painter.drawText(sec_rect, Qt.AlignCenter, image_type)

        # reviewed tag
        if not reviewed:
            text = 'not reviewed'
            tbr = self.metrics.tightBoundingRect(text)  # type QRectF
            sec_width = tbr.width() + text_margin * 2
            rect_x = x + self.horizontal_margin
            color = ColorGui.brush_dark_red

            sec_rect = QRectF(rect_x, emblem_rect_y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, text)

        # resight ID box
        if resight_set:
            # Assume the attribute is already upper case
            tbr = self.metrics.tightBoundingRect(str(resight_set))  # type QRectF
            sec_width = tbr.width() + text_margin * 2
            sec_rect_x = x + self.horizontal_margin
            emblem_rect_y = y + self.emblem_height + 10
            color = QColor("#5f6bfe")

            sec_rect = QRectF(sec_rect_x, emblem_rect_y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, str(resight_set))

        # group area ID box
        if group_area:
            tbr = self.metrics.tightBoundingRect(str(group_area))  # type QRectF
            sec_width = tbr.width() + text_margin * 2
            sec_rect_x = x + self.horizontal_margin
            emblem_rect_y = y + self.emblem_height * 2 + 10 * 2
            color = ColorGui.color_ortho

            sec_rect = QRectF(sec_rect_x, emblem_rect_y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, str(group_area))

        # Object Info on the top
        tbr = self.metrics.tightBoundingRect(object_type)  # type QRectF
        sec_width = tbr.width() + text_margin * 2
        emblem_rect_x_top = x + self.horizontal_margin
        color = ColorGui.color_object
        sec_rect = QRectF(emblem_rect_x_top, y, sec_width, self.emblem_height)
        path = QPainterPath()
        path.addRoundedRect(sec_rect, 5, 5)
        painter.fillPath(path, color)
        painter.drawText(sec_rect, Qt.AlignCenter, object_type)

        # Source
        sec_rect_x = emblem_rect_x_top + sec_width
        text = source_switch(source)
        tbr = self.metrics.tightBoundingRect(text)  # type QRectF
        sec_width = tbr.width() + text_margin * 2
        sec_rect_x = sec_rect_x + 10
        color = ColorGui.color_source
        sec_rect = QRectF(sec_rect_x, y, sec_width, self.emblem_height)
        path = QPainterPath()
        path.addRoundedRect(sec_rect, 5, 5)
        painter.fillPath(path, color)
        painter.drawText(sec_rect, Qt.AlignCenter, text)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return self.fixedSizeHint

    def get_left_point(self, rect: QRect) -> QPointF:
        return QPointF(
            rect.x() + self.horizontal_margin,
            rect.y() + self.image_height + icon_footer_padding - 1,
        )


class CustomSortFilterProxyModel(QSortFilterProxyModel):
    """
    Implements a QSortFilterProxyModel that allows for custom
    filtering. Add new filter functions using addFilterFunction().
    New functions should accept two arguments, the column to be
    filtered and the currently set filter string, and should
    return True to accept the row, False otherwise.
    Filter functions are stored in a dictionary for easy
    removal by key. Use the addFilterFunction() and
    removeFilterFunction() methods for access.
    The filterString is used as the main pattern matching
    string for filter functions. This could easily be expanded
    to handle regular expressions if needed.
    """

    def __init__(self, parent=None):
        super(CustomSortFilterProxyModel, self).__init__(parent)
        self.filter_data = {}
        self.connections = []
        self.filterFunctions = {}

    def setSourceModel(self, model):
        if self.sourceModel() is not None:
            self.sourceModel().rowsRemoved.disconnect()
            self.sourceModel().modelReset.disconnect()
            self.sourceModel().rowsInserted.disconnect()
        QSortFilterProxyModel.setSourceModel(self, model)
        if self.sourceModel() is None:
            self.connections = []
            return
        self.connections = [
            # self.sourceModel().dataChanged.connect(self.sourceDataChanged),
            self.sourceModel().rowsRemoved.connect(self.reload_model),
            self.sourceModel().modelReset.connect(self.reload_model),
            self.sourceModel().rowsInserted.connect(self.reload_model)
        ]
        self.reload_model()

    # def mapFromSource(self, source):
    #   return self.index(source.row(), source.column(), source.parent())

    # def mapToSource(self, proxy):
    #    if not proxy.isValid() and not self.sourceModel():
    #        return QModelIndex()
    #   return self.sourceModel().index(proxy.row(), proxy.column(), proxy.parent())

    def reload_model(self):
        self.beginResetModel()
        # self.buildMap(self.sourceModel())
        self.endResetModel()

    def set_filter_data(self, filter_data):
        """
        text : string
            The string to be used for pattern matching.
        """
        self.filter_data = filter_data
        self.invalidateFilter()

    def add_filter_function(self, name, new_func):
        """
        name : hashable object
            The object to be used as the key for
            this filter function. Use this object
            to remove the filter function in the future.
            Typically, this is a self-descriptive string.
        new_func : function
            A new function which must take two arguments,
            the row to be tested and the ProxyModel's current
            filterString. The function should return True if
            the filter accepts the row, False otherwise.
            ex:
            model.addFilterFunction(
                'test_columns_1_and_2',
                lambda r,s: (s in r[1] and s in r[2]))
        """
        self.filterFunctions[name] = new_func
        self.invalidateFilter()

    def remove_filter_function(self, name):
        """
        name : hashable object

        Removes the filter function associated with name,
        if it exists.
        """
        if name in self.filterFunctions.keys():
            del self.filterFunctions[name]
            self.invalidateFilter()

    def filterAcceptsRow(self, row_num, parent):
        """
        Reimplemented from base class to allow the use
        of custom filtering.
        """
        model = self.sourceModel()
        # The source model should have a method called row()
        # which returns the table row as a python list.
        # tests = [func(model.row(row_num), self.filterString)
        #         for func in self.filterFunctions.values()]
        # return all(tests)
        return self.filter_func(model.row(row_num), self.filter_data)

    def filter_func(self, data: GalleryData, filter_function):
        data = data.__dict__
        for key in filter_function:
            if key in ["source", "image_type", "active"]:
                if data[key] not in filter_function[key]:
                    return False
            elif key == "object_type":

                # When we submit new object for the time before setting object type it is None
                # So we need to check that because None has not lower value
                if data[key] is None:
                    return False
                if filter_function[key].lower() not in data[key].lower():
                    return False
            elif key == "reviewed":
                if data[key] == filter_function[key]:
                    return False
            else:
                if data[key] != filter_function[key]:
                    return False
        return True


def gallery_loader(db: DBHandler, order_value='id'):
    objects = db.load_objects_all_sort_by_group(order_value=order_value)

    # We want to order 0 group ids ad the end
    if order_value in ['resight_set', 'group_area']:

        objects_resight_set = []
        objects_no_resight_set = []
        for single_object in objects:
            if single_object[order_value] == 0:
                objects_no_resight_set.append(single_object)
            else:
                objects_resight_set.append(single_object)

        objects = objects_resight_set + objects_no_resight_set

    entries = []
    for single_object in objects:
        data = GalleryData()
        #pixmap = QPixmap()
        #pixmap.loadFromData(single_object['cropped_image'], "JPG")
        #data.thumbnail = pixmap
        data.id = single_object['id']
        data.image = single_object['image']
        data.folder = single_object['img_path']

        image_type = ImageType(0).fullname
        if single_object['math_model']:
            math_model = json.loads(single_object['math_model'])

            image_type = math_model.get('type', ImageType(0).fullname)

        data.image_type = image_type
        data.source = single_object['source']
        data.active = single_object['active']
        data.tags = single_object['tags']
        data.highlighted = single_object['highlighted']
        data.group_area = single_object['group_area']
        data.resight_set = single_object['resight_set']
        data.extension = Path(single_object['img_path']).suffix[1:]
        data.reviewed = single_object['reviewed']

        data.object_type = single_object['object_type']
        entries.append(data)

    model = GalleryListModel(entries)

    return model


def gallery_loader_single(db: DBHandler, object_id) -> GalleryData:
    obj = db.load_objects_single_object(object_id)

    data = GalleryData()
    #pixmap = QPixmap()
    #pixmap.loadFromData(obj['cropped_image'], "JPG")
    #data.thumbnail = pixmap
    data.id = obj['id']
    data.image = obj['image']
    data.folder = obj['img_path']

    # TODO maybe again add image type to db as own entry
    image_type = ImageType.Unknown.fullname
    if obj['math_model']:
        math_model = json.loads(obj['math_model'])

        image_type = math_model.get('type', 'unknown')

    data.image_type = image_type
    data.source = obj['source']
    data.active = obj['active']
    data.tags = obj['tags']
    data.highlighted = obj['highlighted']
    data.group_area = obj['group_area']
    data.resight_set = obj['resight_set']
    data.extension = Path(obj['img_path']).suffix[1:]

    data.object_type = obj['object_type']
    data.reviewed = obj['reviewed']

    return data
