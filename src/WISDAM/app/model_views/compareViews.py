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


import json

from PySide6.QtCore import (
    QAbstractTableModel)
from PySide6.QtCore import (
    QModelIndex,
    QSizeF,
    QSize,
    QRect,
    QRectF,
    QPointF,
    Qt, QAbstractListModel, Signal, SignalInstance
)
from PySide6.QtGui import (
    QPainter,
    QFontMetricsF,
    QFont,
    QIcon,
    QPixmap, QPen, QPainterPath)
from PySide6.QtWidgets import (
    QListView,
    QStyledItemDelegate,
    QStyleOptionViewItem, QFrame, QStyle)

from app.var_classes import (GalleryIconSize, ColorGui, source_switch,
                             icon_footer_padding, spacing_grid,
                             icon_margin, text_margin)

from db.dbHandler import DBHandler

from compare.utils import CompareIconRole, CompareList, CompareIconData, RolesComparePane

from pathlib import Path

from PySide6.QtCore import Qt


# List View for Items
class CompareIconDelegate(QStyledItemDelegate):
    """
    Render thumbnail cells
    """

    def __init__(self, parent=None, thumb_size=GalleryIconSize) -> None:
        super().__init__(parent)

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

        self.emblemFont = QFont()
        self.emblemFont.setPointSize(self.emblemFont.pointSize())
        self.emblemFont.setBold(False)
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

        thumbnail = index.data(CompareIconRole.thumbnail)
        valid = index.data(CompareIconRole.valid)
        text = index.data(CompareIconRole.text)
        object_type = index.data(CompareIconRole.object_type)
        group_ident = index.data(CompareIconRole.group_ident)

        x = option.rect.x()
        y = option.rect.y()

        painter.setRenderHint(QPainter.Antialiasing, True)

        thumbnail_x = (self.horizontal_margin + x)
        thumbnail_y = (self.vertical_margin + y)

        # Draw rectangle in which the individual items will be placed
        box_rect = QRectF(x + 1.5, y + 1.5, self.width - 3, self.height - 3)

        painter.setRenderHint(QPainter.Antialiasing, True)

        if valid == 1:
            painter.setPen(QPen(ColorGui.color_dark_green, 3))
        elif valid < 0:
            painter.setPen(QPen(ColorGui.color_mid_yellow, 3))
        else:
            painter.setPen(QPen(ColorGui.color_dark_red, 3))

        painter.drawRect(box_rect)

        painter.setFont(self.emblemFont)

        # If mouse is over the item than show item and few texts
        if not (option.state & QStyle.StateFlag.State_MouseOver):
            target = QRectF(thumbnail_x, thumbnail_y, self.width - self.horizontal_margin * 2,
                            self.height - self.vertical_margin * 2)
            size = thumbnail.size().scaled(target.width(), target.height(), Qt.KeepAspectRatio)
            painter.drawPixmap(target.x(), target.y(), size.width(), size.height(), thumbnail)

            painter.setPen("white")
            tbr = self.metrics.tightBoundingRect(object_type)  # type QRectF
            sec_width = tbr.width() + text_margin * 2
            emblem_rect_x_top = x + self.horizontal_margin
            color = ColorGui.color_object
            sec_rect = QRectF(emblem_rect_x_top, y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, object_type)

            if group_ident:
                text = "group " + str(index.data(CompareIconRole.group_ident))
                color = ColorGui.color_dark_green
                emblem_rect_y = y + self.emblem_height + 10
                tbr = self.metrics.tightBoundingRect(text)  # type QRectF
                sec_width = tbr.width() + text_margin * 2
                emblem_rect_x_top = x + self.horizontal_margin
                sec_rect = QRectF(emblem_rect_x_top, emblem_rect_y, sec_width, self.emblem_height)
                path = QPainterPath()
                path.addRoundedRect(sec_rect, 5, 5)
                painter.fillPath(path, color)
                painter.drawText(sec_rect, Qt.AlignCenter, text)

        else:
            emblem_rect = QRectF(thumbnail_x, thumbnail_y,
                                 self.width - self.horizontal_margin * 2, self.height - self.vertical_margin * 2)
            painter.setPen('white')
            painter.drawText(emblem_rect, Qt.AlignLeft, text)

        painter.restore()

    def sizeHint(self, option: QStyleOptionViewItem, index: QModelIndex) -> QSize:
        return self.fixedSizeHint

    def get_left_point(self, rect: QRect) -> QPointF:
        return QPointF(
            rect.x() + self.horizontal_margin,
            rect.y() + self.image_height + icon_footer_padding - 1,
        )


class CompareIconModel(QAbstractListModel):
    def __init__(self, data):
        super(CompareIconModel, self).__init__()
        self._data = data

        # self.rows = self._data

    def rowCount(self, parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def flags(self, index: QModelIndex) -> Qt.ItemFlags:
        if not index.isValid():
            return Qt.ItemFlag.NoItemFlags

        row = index.row()
        if row >= len(self._data) or row < 0:
            return Qt.ItemFlag.NoItemFlags

        return super().flags(index) | Qt.ItemIsEnabled | Qt.ItemIsSelectable

    def append_data(self, data: CompareIconData):
        self.layoutAboutToBeChanged.emit()
        self._data.append(data)
        self.layoutChanged.emit()

    def row(self, row: int):
        """
        get row
        """
        return self._data[row]

    def get_data(self) -> list[CompareIconData]:
        return self._data

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row_id = index.row()
        if row_id >= len(self._data) or row_id < 0:
            return None

        row = self._data[row_id]
        if role == CompareIconRole.thumbnail:
            return row.thumbnail
        elif role == CompareIconRole.id:
            return row.id
        elif role == CompareIconRole.valid:
            return row.valid
        elif role == CompareIconRole.text:
            return row.text
        elif role == CompareIconRole.index:
            return row.index
        elif role == CompareIconRole.object_type:
            return row.object_type
        elif role == CompareIconRole.group_ident:
            return row.group_ident

    def set_all_no_valid(self):

        self.layoutAboutToBeChanged.emit()
        for row in self._data:
            row.valid = 0
        self.layoutChanged.emit()
        return True

    def set_valid(self, index: QModelIndex, valid: int):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        self._data[row].valid = valid
        self.layoutChanged.emit()
        return True


class CompareListView(QListView):
    change_valid: SignalInstance = Signal(object, int, int)
    valid_all_no: SignalInstance = Signal(object)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setSpacing(spacing_grid)
        self.setIconSize(QSize(GalleryIconSize.width, GalleryIconSize.height))
        self.possiblyPreserveSelectionPostClick = False
        self.user_visible_columns = 0
        self.setFrameShadow(QFrame.Shadow.Plain)

        self.index_cmp_table = None

    def mousePressEvent(self, event):

        if self.model() is not None:

            if self.indexAt(event.pos()).isValid():

                index = self.indexAt(event.pos())

                index_model = index.model()

                valid = index.data(CompareIconRole.valid)
                id_obj = index.data(CompareIconRole.id)
                persistent_index_cmp_table = index.data(CompareIconRole.index)

                if event.button() == Qt.LeftButton:
                    # Ids are not sorted, so we must look for ids to set it

                    if valid:
                        index_model.set_all_no_valid()
                        self.valid_all_no.emit(persistent_index_cmp_table)
                    else:
                        valid = 1
                        index_model.set_valid(index, valid)
                        self.change_valid.emit(persistent_index_cmp_table, id_obj, valid)

                # With the right button the splitting is set for that object
                if event.button() == Qt.RightButton:

                    if valid >= 0:
                        valid = -1
                    else:
                        valid = 0

                    index_model.set_valid(index, valid)
                    self.change_valid.emit(persistent_index_cmp_table, id_obj, valid)

        super(CompareListView, self).mousePressEvent(event)

    def resizeEvent(self, event) -> None:
        """
        Resize, then calculate and store how many columns the user sees
        """
        super().resizeEvent(event)


def compare_image_loader(db_path: Path, index, ids, valids, table_ai=False):
    db = DBHandler.from_path(db_path, '')

    if table_ai:
        data = db.load_ai_detections_ids(ids)
    else:
        data = db.load_objects_ids(ids)

    entries = []

    for idx, x in enumerate(data):

        pixmap = QPixmap()
        pixmap.loadFromData(x['cropped_image'], "JPG")

        # The item text will later be displayed if the user hovers over the icon
        # Will be stored in the UserRole Text
        if 'source' in x.keys():
            item_text = 'Source: ' + source_switch(x['source'])
        else:
            item_text = 'Source: AI'
        item_text += '\t\t\t\t\tImage: ' + str(x['image'])
        item_text += '\nUser: ' + str(x['user'])

        if not table_ai:
            item_text += '\nGroup: ' + str(x['resight_set'])
        item_text += '\t\t\t\t\tTaxa: ' + x['object_type']
        if table_ai:
            item_text += '\t\t\t\t\tTaxa AI: ' + x['object_type_orig']
        item_text += '\n'
        if x['data']:
            meta_data = json.loads(x['data'])
            data_number = 0
            for key, value in meta_data.items():
                new_row = '\t\t\t\t\t'
                if data_number % 2 == 0:
                    new_row = '\n'
                item_text += new_row + str(key) + ': ' + str(value)
                data_number += 1

        data_icon = CompareIconData()
        data_icon.thumbnail = pixmap
        data_icon.index = index
        data_icon.id = x['id']
        data_icon.valid = valids[ids.index(x['id'])]
        data_icon.text = item_text
        data_icon.object_type = x['object_type']

        data_icon.group_ident = 0
        if 'resight_set' in x.keys():
            data_icon.group_ident = x['resight_set']

        entries.append(data_icon)

    if entries:
        model = CompareIconModel(entries)

        return model

    return None


class CompareIconCenterDelegate(QStyledItemDelegate):
    def initStyleOption(self, option, index):
        super(CompareIconCenterDelegate, self).initStyleOption(option, index)
        option.decorationPosition = QStyleOptionViewItem.Right
        option.decorationAlignment = (Qt.AlignVCenter | Qt.AlignCenter)
        option.displayAlignment = (Qt.AlignVCenter | Qt.AlignCenter)


class CompareListModel(QAbstractTableModel):
    def __init__(self, data, header):
        super(CompareListModel, self).__init__()
        self._data = data
        self._header = header

    def append_data(self, data):
        self._data.append(data)
        self.layoutChanged.emit()

    def data(self, index, role):

        if role == Qt.TextAlignmentRole:
            if index.column() in [CompareList.db, CompareList.seen, CompareList.groups_involved, CompareList.nrs_db1]:
                return Qt.AlignCenter

        if role == Qt.BackgroundRole:

            if index.column() == CompareList.nrs_db1:
                if self._data[index.row()][CompareList.nrs_db1] > 1:
                    return ColorGui.color_mid_yellow
            if index.column() == CompareList.nrs_db2:
                if self._data[index.row()][CompareList.nrs_db2] > 1:
                    return ColorGui.color_mid_yellow

            if index.column() == CompareList.type:
                list1 = list(set(self._data[index.row()][CompareList.type]))
                list2 = list(set(self._data[index.row()][CompareList.type_other]))
                list1.sort()
                list2.sort()

                if len(list1) > 1 or len(list2) > 1 or (len(list1) > 1 and len(list2) > 1 and list1 != list2):
                    return ColorGui.brush_dark_red
                else:
                    return ColorGui.brush_light_green

            if index.column() == CompareList.groups_involved:
                if self._data[index.row()][CompareList.groups_involved] == 'yes':
                    return ColorGui.color_mid_blue

            if index.column() == CompareList.id:
                flag_valid = self._data[index.row()][CompareList.flag_valid]
                seen = self._data[index.row()][CompareList.seen]

                if seen:
                    if flag_valid:
                        return ColorGui.brush_light_green
                    else:
                        return ColorGui.brush_dark_red

        if role == RolesComparePane.id:
            return self._data[index.row()][CompareList.id]

        if role == RolesComparePane.flag_fit:
            return self._data[index.row()][CompareList.flag_valid]

        if role == RolesComparePane.c1_ids:
            return self._data[index.row()][CompareList.c1_ids]

        if role == RolesComparePane.c2_ids:
            return self._data[index.row()][CompareList.c2_ids]

        if role == RolesComparePane.c1_valid:
            return self._data[index.row()][CompareList.c1_valid]

        if role == RolesComparePane.c2_valid:
            return self._data[index.row()][CompareList.c2_valid]

        if role == Qt.DisplayRole:
            if index.column() in [CompareList.id, CompareList.groups_involved, CompareList.db,
                                  CompareList.nrs_db1, CompareList.nrs_db2]:
                return self._data[index.row()][index.column()]
            if index.column() == CompareList.type:
                if self._data[index.row()][index.column()]:
                    return self._data[index.row()][CompareList.type][0]
                else:
                    return self._data[index.row()][CompareList.type_other][0]

        if role == Qt.DecorationRole:
            value = self._data[index.row()][index.column()]

            nr2 = self._data[index.row()][CompareList.nrs_db2]
            nr1 = self._data[index.row()][CompareList.nrs_db1]

            if index.column() == CompareList.nrs_db1:

                if not nr2 or not nr1:
                    return QIcon(u":icons/icons/flat_cross_icon.svg")
                else:
                    return QIcon(u":icons/icons/flat_tick_icon.svg")

            # was revisited
            if index.column() == CompareList.seen:
                # if isinstance(value, bool):
                if value:
                    return QIcon(u":icons/icons/flat_tick_icon_yellow.svg")

    def change_value(self, index, value):
        self._data[index.row()][index.column()] = value
        self.layoutChanged.emit()

    def change_row(self, index, value):
        self._data[index.row()] = value
        self.layoutChanged.emit()

    def change_valid(self, index, id_obj, value, compare_source):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        if compare_source == 0:
            ids = index.data(RolesComparePane.c1_ids)
            valid = index.data(RolesComparePane.c1_valid)
            valid[ids.index(id_obj)] = value
            self._data[index.row()][CompareList.c1_valid] = valid
        else:
            ids = index.data(RolesComparePane.c2_ids)
            valid = index.data(RolesComparePane.c2_valid)
            valid[ids.index(id_obj)] = value
            self._data[index.row()][CompareList.c2_valid] = valid
        self.layoutChanged.emit()

    def set_all_no_valid(self, index, compare_source):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        if compare_source == 0:
            valids = self._data[index.row()][CompareList.c1_valid]
            self._data[index.row()][CompareList.c1_valid] = [0] * len(valids)
        else:
            valids = self._data[index.row()][CompareList.c2_valid]
            self._data[index.row()][CompareList.c2_valid] = [0] * len(valids)

        self.layoutChanged.emit()

    def headerData(self, col, orientation, role):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._header[col]
        return None

    def rowCount(self, index):
        # The length of the outer list.
        return len(self._data)

    def columnCount(self, index):
        # The following takes the first sub-list, and returns
        # the length (only works if all rows are an equal length)
        return len(self._data[0])

    def removeRows(self, position, rows, model_index: QModelIndex):
        self.layoutAboutToBeChanged.emit()
        self.beginRemoveRows(model_index, position, position + rows - 1)
        for i in range(rows):
            del (self._data[position])
        self.endRemoveRows()
        self.layoutChanged.emit()
        return True

    def get_data(self) -> list:
        return self._data




