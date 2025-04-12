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


from PySide6.QtCore import (
    QAbstractListModel,
    QModelIndex,
    Signal,
    QSizeF,
    QSize,
    QRect,
    QRectF,
    Slot,
    QSortFilterProxyModel,
    QPersistentModelIndex,
    QPointF, Qt
)
from PySide6.QtWidgets import (
    QListView,
    QStyledItemDelegate,
    QStyleOptionViewItem,
    QMenu,
    QFrame

)
from PySide6.QtGui import (
    QPainter,
    QFontMetricsF,
    QFont,
    QPainterPath,
    QPixmap, QColor, QPen
)

# Classes and Modules
from db.dbHandler import DBHandler
from app.var_classes import (AiRoles, AIData, AISize, ColorGui, icon_margin,
                             icon_footer_padding, text_margin, spacing_grid)
from app.popups.popupTextInput import POPUPTextInput


class AIListModel(QAbstractListModel):
    def __init__(self, data):
        super(AIListModel, self).__init__()
        self._data: list[AIData] = data

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

    def append_data(self, data: AIData):
        self._data.append(data)
        self.layoutChanged.emit()

    def row(self, row: int):
        """
        get row
        """
        return self._data[row]

    def get_data(self) -> list[AIData]:
        return self._data

    def nr_imported(self) -> int:

        return len([1 for x in self._data if x.imported])

    def get_nr_ai_runs(self) -> int:

        ai_runs = []

        for x in self._data:
            ai_runs.append(x.ai_run)

        return len(set(ai_runs))

    def data(self, index: QModelIndex, role=Qt.DisplayRole):
        if not index.isValid():
            return None

        row_id = index.row()
        if row_id >= len(self._data) or row_id < 0:
            return None

        row = self._data[row_id]
        if role == AiRoles.id:
            return row.id
        elif role == AiRoles.object_type:
            return row.object_type
        elif role == AiRoles.active:
            return row.active
        elif role == AiRoles.probability:
            return row.probability
        elif role == AiRoles.ai_run:
            return row.ai_run
        elif role == AiRoles.imported:
            return row.imported
        # elif role == Roles.starred:
        #    return row.starred
        elif role == AiRoles.image_id:
            return row.image_id

        elif role == AiRoles.thumbnail:
            return row.thumbnail

    def change_value(self, index: QModelIndex, value):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        if row >= len(self._data) or row < 0:
            return False
        self._data[index.row()][index.column()] = value
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

    def set_object_type(self, index: QModelIndex, value):
        if not index.isValid():
            return False
        self.layoutAboutToBeChanged.emit()
        row = index.row()
        self._data[row].object_type = value
        self.layoutChanged.emit()
        return True

    # def setStarred(self, index: QModelIndex, value):
    #    if not index.isValid():
    #        return False
    #    self.layoutAboutToBeChanged.emit()
    #    row = index.row()
    #    self._data[row].starred = value
    #    self.layoutChanged.emit()
    #    return True

    def remove_row_ai_id(self, ai_id, model_index: QModelIndex):
        """
        Removes Python list rows only, i.e. self.rows.

        Does not touch database or other variables.
        """
        self.layoutAboutToBeChanged.emit()
        position = None
        for idx, row in enumerate(self._data):
            if row.id == ai_id:
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


class AIView(QListView):
    """
    Thumbnail view. QListView in icon mode.
    """

    # Signals
    goto_image = Signal(int)

    def __init__(self, parent=None):
        super().__init__(parent)

        # Define view mode
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setUniformItemSizes(True)
        self.setSpacing(spacing_grid)
        self.setIconSize(QSize(AISize.width, AISize.height))

        self.setFrameShadow(QFrame.Shadow.Plain)
        self.fast_activate = False
        self.clickedIndex = QPersistentModelIndex()

        # self.possiblyPreserveSelectionPostClick = False

        # Track how many columns the user sees
        # QListView IconMode indexes are always set to column 0
        self.user_visible_columns = 0
        self._db: DBHandler | None = None
        self.contextMenu = QMenu()

    def set_db(self, db: DBHandler):
        self._db = db

    def mousePressEvent(self, event):

        index = self.indexAt(event.pos())
        if index.isValid():
            self.clickedIndex = QPersistentModelIndex(index)

            # Left button will activate/deactivate the AI detection
            if event.button() == Qt.LeftButton:
                self.activate()

            # Right button will open the context menu only if it is not imported
            if event.button() == Qt.RightButton:
                if index.isValid():
                    self.contextMenu = QMenu()

                    if self.clickedIndex.isValid() and not self.clickedIndex.data(AiRoles.imported):
                        text = "Change Metadata"
                        change_meta_data_act = self.contextMenu.addAction(text)
                        change_meta_data_act.triggered.connect(self.change_meta_data)

                        global_pos = self.mapToGlobal(event.pos())
                        self.contextMenu.popup(global_pos)

        super().mousePressEvent(event)

    @Slot()
    def activate(self):
        index = self.clickedIndex
        if index.isValid():
            index_model = index.model().mapToSource(index)
            if not index_model.data(AiRoles.imported):
                active = 0 if index_model.data(AiRoles.active) else 1
                self.update(index)
                index.model().sourceModel().set_active(index_model, 0 if index_model.data(AiRoles.active) else 1)
                self._db.set_active_ai(active, index_model.data(AiRoles.id))


    @Slot()
    def change_meta_data(self) -> None:
        index = self.clickedIndex
        if index.isValid():
            pass
            index_model = index.model().mapToSource(index)
            if not index_model.data(AiRoles.imported):

                v = POPUPTextInput()
                if v.exec_():  # Execution method becomes a modal dialog box.After the user clicks OK, he returns  to 1.
                    name = v.get_data()
                    if name:
                        index.model().sourceModel().set_object_type(index_model, name)
                        self._db.change_ai_data(index_model.data(AiRoles.id), name)

    def resizeEvent(self, event) -> None:
        """
        Resize, then calculate and store how many columns the user sees
        """
        super().resizeEvent(event)


class AIDelegate(QStyledItemDelegate):
    """
    Render thumbnail cells of AI detections
    """

    def __init__(self, parent=None, icon_size=AISize, db: DBHandler = None) -> None:
        super().__init__(parent)

        self.labels_visible = True

        self.image_width = icon_size.width
        self.image_height = icon_size.height
        self.horizontal_margin = float(icon_margin)
        self.vertical_margin = float(icon_margin)
        self.db: DBHandler | None = db

        self.width = self.image_width + self.horizontal_margin * 2
        self.height = self.image_height + self.vertical_margin * 2

        self.emblemFont = QFont()
        self.emblemFont.setPointSize(self.emblemFont.pointSize() + 3)
        self.emblemFont.setBold(True)
        metrics = QFontMetricsF(self.emblemFont)

        # Determine the actual height of the font
        ext = "aaaa".upper()
        tbr = metrics.tightBoundingRect(ext)
        self.emblem_height = tbr.height() * 2

        # Size is always fixed, so calculate it here
        self.fixedSizeHint = QSizeF(self.width, self.height).toSize()

    def toggle_labels(self):
        self.labels_visible = not self.labels_visible

    def paint(self, painter: QPainter, option: QStyleOptionViewItem, index: QModelIndex) -> None:
        # super().paint(painter, option, index)
        if index is None:
            return

        if not index.isValid():
            return

        # Save state of painter, restore on function exit
        painter.save()

        ai_detection_id = index.data(AiRoles.id)
        active = index.data(AiRoles.active)
        ai_run = index.data(AiRoles.ai_run)
        image_id = index.data(AiRoles.image_id)
        object_type = index.data(AiRoles.object_type)
        thumbnail = index.data(AiRoles.thumbnail)
        # starred = index.data(Roles.starred)
        probability = index.data(AiRoles.probability)
        imported = index.data(AiRoles.imported)

        x = option.rect.x()
        y = option.rect.y()

        # Draw rectangle in which the individual items will be placed
        box_rect = QRectF(x, y, self.width, self.height)
        painter.setRenderHint(QPainter.Antialiasing, True)
        if active and not imported:

            painter.setPen(QPen(ColorGui.color_active, 3))
        elif imported:

            painter.setPen(QPen(ColorGui.color_imported, 3))
            # painter.fillRect(box_rect, ColorGui.color_imported)
        else:
            painter.setPen(QPen(ColorGui.color_not_active, 3))

        painter.drawRect(box_rect)

        thumbnail_x = (self.horizontal_margin + x)
        thumbnail_y = (self.vertical_margin + y)

        target = QRectF(thumbnail_x, thumbnail_y, self.width - self.horizontal_margin * 2,
                        self.height - self.vertical_margin * 2)
        # painter.drawPixmap(target.toRect(), thumbnail)

        if self.db is not None:
            thumbnail_db = self.db.get_cropped_image_ai(ai_detection_id)
            if thumbnail_db:
                thumbnail = QPixmap()
                thumbnail.loadFromData(thumbnail_db['image_detection'], "JPG")

        if thumbnail is not None:
            size = thumbnail.size().scaled(target.width(), target.height(), Qt.KeepAspectRatio)
            painter.drawPixmap(target.x(), target.y(), size.width(), size.height(), thumbnail)

        if self.labels_visible:
            # Draw a small coloured box containing the file extension in the
            # bottom right corner
            extension = str(ai_run)
            # Calculate size of extension text
            painter.setFont(self.emblemFont)
            # em_width = self.emblemFontMetrics.width(extension)
            metrics = QFontMetricsF(self.emblemFont)
            tbr = metrics.tightBoundingRect(extension)
            emblem_width = tbr.width() + text_margin * 2
            emblem_rect_x = self.width - self.horizontal_margin - emblem_width + x
            emblem_rect_y = y + self.image_height - icon_footer_padding

            emblem_rect = QRectF(emblem_rect_x, emblem_rect_y, emblem_width, self.emblem_height)
            color = ColorGui.color_extension
            path = QPainterPath()
            path.addRoundedRect(emblem_rect, 5, 5)
            painter.fillPath(path, color)
            painter.setPen(QColor(Qt.white))
            painter.drawText(emblem_rect, Qt.AlignCenter, extension)

            # Object Info on the top
            tbr = metrics.tightBoundingRect(object_type)
            sec_width = tbr.width() + text_margin * 2
            emblem_rect_x_top = x + self.horizontal_margin
            color = ColorGui.color_object
            sec_rect = QRectF(emblem_rect_x_top, y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, object_type)

            # Image ID on the top
            tbr = metrics.tightBoundingRect(str(image_id))  # type: QRectF
            sec_width = tbr.width() + text_margin * 2
            emblem_rect_x_top = x + self.horizontal_margin
            emblem_rect_y = y + self.image_height - icon_footer_padding
            color = ColorGui.brush_dark_green
            sec_rect = QRectF(emblem_rect_x_top, emblem_rect_y, sec_width, self.emblem_height)
            path = QPainterPath()
            path.addRoundedRect(sec_rect, 5, 5)
            painter.fillPath(path, color)
            painter.drawText(sec_rect, Qt.AlignCenter, str(image_id))

            # Object Info on the top - Probability
            text = '%i' % int(probability * 100) + '%'
            tbr = metrics.tightBoundingRect(text)  # type: QRectF
            sec_width = tbr.width() + text_margin * 2
            emblem_rect_x = self.width - self.horizontal_margin - sec_width + x
            color = ColorGui.color_object
            sec_rect = QRectF(emblem_rect_x, y, sec_width, self.emblem_height)
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


class AICustomSortFilterProxyModel(QSortFilterProxyModel):
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
        super(AICustomSortFilterProxyModel, self).__init__(parent)
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
            Typically this is a self descriptive string.
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

    @staticmethod
    def filter_func(data: AIData, filter_in):
        data = data.__dict__
        for key in filter_in:
            if key in ["imported", "active"]:
                if data[key] not in filter_in[key]:
                    return False
            elif key == "object_type":
                if filter_in[key].lower() not in data[key].lower():
                    return False
            elif key == "probability":
                if 'prob_lower' in filter_in.keys():
                    if data[key] > filter_in[key]:
                        return False
                else:
                    if data[key] < filter_in[key]:
                        return False
            else:
                if key in data.keys():
                    if data[key] != filter_in[key]:
                        return False
        return True


def ai_loader(db: DBHandler):
    if db is not None:
        ai_detections = db.load_ai_detections(sort_by_image=True)
        entries = []
        for x in ai_detections:
            data = AIData()

            # We do not load anymore a pixmap
            # Now in the paint event we will directly access the database
            # Otherwise for very large datasets the programm would run out of memory and take long time to load
            #pix_map = QPixmap()
            # pix_map.loadFromData(x['image_detection'], "JPG")
            #data.thumbnail = pix_map  # .scaledToWidth(pix_map.width()/2.0, mode=Qt.SmoothTransformation)
            data.id = x['id']
            data.ai_run = x['ai_run']
            data.active = x['active']
            data.object_type = x['object_type']
            data.probability = x['probability']
            data.imported = x['imported']
            data.image_id = x['image']

            entries.append(data)

        model = AIListModel(entries)

        # fddvcmodel.append_data()

        return model
    return None
