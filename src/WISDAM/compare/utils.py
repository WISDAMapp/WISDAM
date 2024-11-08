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


from enum import IntEnum
from pathlib import Path
from PySide6.QtCore import Qt


dist_compare_search = 100


class CompareType:

    def __init__(self, ai: bool, path: Path):

        self.ai = ai
        self.db: Path | None = path


class CompareSighting:

    def __init__(self, id_comp, image, img_path, meta_type, object_type, resight_set, geometry, data, data_env):
        self.id = id_comp
        self.image = image
        self.img_path = img_path
        self.meta_type = meta_type
        self.object_type = object_type
        self.resight_set = resight_set
        self.geometry = geometry
        self.data = data
        self.data_env = data_env


class CompareList:
    id = 0
    type = 1
    db = 2
    seen = 3
    nrs_db1 = 4
    nrs_db2 = 5
    groups_involved = 6
    c1_ids = 7
    c2_ids = 8
    flag_valid = 9
    type_other = 10
    c1_valid = 11
    c2_valid = 12
    c1_group = 13
    c2_group = 14
    c1_image = 15
    c2_image = 16
    c1_data = 17
    c2_data = 18
    c1_data_env = 19
    c2_data_env = 20


compare_list_header = ['first obj. ID', 'Type', 'DB', 'Seen', 'Nrs. DB1', 'Nrs. DB2', 'Groups',
                       'c1_ids', 'c2_ids', 'valid', 'type_other', 'c1_valid', 'c2_valid',
                       'c1_group', 'c2_group', 'c1_image', 'c2_image', 'c1_data', 'c2_data',
                       'c1_data_env', 'c2_data_env']


class CompareData:
    id = 0
    image = 0
    active = 0
    image_type = 0
    source = 0
    extension = 'JPG'
    object_type = 'none'
    group_area = []
    resight_set = []
    thumbnail = []
    tags = {}
    highlighted = 0
    folder = ""


class CompareIconData:
    thumbnail = None
    index = 0
    id = 0
    valid = []
    text = ''
    object_type = ''
    group_ident = 0


class CompareIconRole(IntEnum):
    thumbnail = Qt.ItemDataRole.UserRole + 1
    index = Qt.ItemDataRole.UserRole + 2
    id = Qt.ItemDataRole.UserRole + 3
    valid = Qt.ItemDataRole.UserRole + 4
    text = Qt.ItemDataRole.UserRole + 5
    object_type = Qt.ItemDataRole.UserRole + 6
    group_ident = Qt.ItemDataRole.UserRole + 7


class RolesComparePane(IntEnum):
    id = Qt.ItemDataRole.UserRole + 1
    c1_ids = Qt.ItemDataRole.UserRole + 2
    c2_ids = Qt.ItemDataRole.UserRole + 3
    flag_fit = Qt.ItemDataRole.UserRole + 4
    c1_valid = Qt.ItemDataRole.UserRole + 5
    c2_valid = Qt.ItemDataRole.UserRole + 6
