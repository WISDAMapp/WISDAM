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
import numpy as np
from shapely import geometry as gm

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import Qt

from db.dbHandler import DBHandler
from app.var_classes import group_area_header


class GroupAreaTable(QAbstractTableModel):

    def __init__(self, data, header):
        super(GroupAreaTable, self).__init__()
        self._data = data
        self._header = header

    def data(self, index, role):

        if role == Qt.DisplayRole:
            # See below for the nested-list data structure.
            # .row() indexes into the outer list,
            # .column() indexes into the sub-list
            return self._data[index.row()][index.column()]

    def changeValue(self, index, value):
        self._data[index.row()][index.column()] = value
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


def loader_group_area(db: DBHandler):
    data = db.obj_load_all()

    dict_area = {}

    group_area_model = []

    for idx, row in enumerate(data):
        grp_area = row['group_area']
        if grp_area != 0:
            if grp_area not in dict_area.keys():
                dict_area[grp_area] = []

            if row['geo'] is not None:
                geom = gm.shape(json.loads(row['geo']))

                dict_area[grp_area].append([[geom.centroid.x,
                                             geom.centroid.y], row['object_type']])

    for key, value in dict_area.items():
        list_coo = [x[0] for x in value]
        str_types = ','.join(list(set([str(x[1]) for x in value])))
        center = np.array(list_coo).mean(axis=0).tolist()

        group_area_model.append([key, len(value), str_types, center])

    if group_area_model:
        model_table = GroupAreaTable(group_area_model, group_area_header)
        return model_table
    else:
        return None
