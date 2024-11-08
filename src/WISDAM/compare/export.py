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
from pathlib import Path
import csv

from compare.utils import CompareList


def compare_export(export_path: Path, db1_path_string, db2_path_string, data):

    # first get all metadata types present by iteration over data and env data
    # this will be the header

    header_object_data_db1 = []
    header_env_data_db1 = []
    
    header_object_data_db2 = []
    header_env_data_db2 = []

    for idx, item in enumerate(data):

        idx_valid1 = 0
        idx_valid2 = 0

        if 1 in item[CompareList.c1_valid]:
            idx_valid1 = item[CompareList.c1_valid].index(1)
        if 1 in item[CompareList.c2_valid]:
            idx_valid2 = item[CompareList.c2_valid].index(1)

        if item[CompareList.c1_ids]:
            if item[CompareList.c1_data][idx_valid1]:
                data_c1: dict = json.loads(item[CompareList.c1_data][idx_valid1])
                header_object_data_db1 += data_c1.keys()
            if item[CompareList.c1_data_env][idx_valid1]:
                data_env_c1 = json.loads(item[CompareList.c1_data_env][idx_valid1])
                header_env_data_db1 += data_env_c1['data'].keys()

        if item[CompareList.c2_ids]:
            if item[CompareList.c2_data][idx_valid2]:
                data_c2 = json.loads(item[CompareList.c2_data][idx_valid2])
                header_object_data_db2 += data_c2.keys()
            if item[CompareList.c2_data_env][idx_valid2]:
                data_env_c2 = json.loads(item[CompareList.c2_data_env][idx_valid2])
                header_env_data_db2 += data_env_c2['data'].keys()

    header_object_data_db1 = list(set(header_object_data_db1))
    header_env_data_db1 = list(set(header_env_data_db1))

    header_object_data_db2 = list(set(header_object_data_db2))
    header_env_data_db2 = list(set(header_env_data_db2))

    if 'certainty' in header_object_data_db1:
        header_object_data_db1.remove('certainty')
    if 'certainty' in header_object_data_db2:
        header_object_data_db2.remove('certainty')

    header_match_data = ['match_' + s for s in header_object_data_db1]
    header_match_env_data = ['match_env_' + s for s in header_env_data_db1]

    header_object_data_db1 = ['db1_' + s for s in list(set(header_object_data_db1))]
    header_env_data_db1 = ['db1_' + s for s in list(set(header_env_data_db1))]

    header_object_data_db2 = ['db2_' + s for s in list(set(header_object_data_db2))]
    header_env_data_db2 = ['db2_' + s for s in list(set(header_env_data_db2))]

    # common headers are currently hardcoded

    fieldnames = ['id', 'db1_path', 'db2_path', 'inspected', 'db1_nr_obj', 'db2_nr_obj',
                  'db1_id_item', 'db1_valid', 'db1_id_image', 'db1_object_type', 'db1_certainty', 'db1_id_resightset']
    fieldnames += header_object_data_db1
    fieldnames += header_env_data_db1
    fieldnames += ['db2_id_item', 'db2_valid', 'db2_id_image', 'db2_object_type', 'db2_certainty',  'db2_id_resightset']
    fieldnames += header_object_data_db2
    fieldnames += header_env_data_db2
    fieldnames += ['match_objectType', 'match_certainty']
    fieldnames += header_match_data
    fieldnames += header_match_env_data

    # empty_dict = dict(zip(dict_keys, [None] * len(dict_keys)))

    # CSV Writer
    with open(export_path, 'w', newline='') as csvfile:

        csv_writer = csv.DictWriter(csvfile, delimiter=',', quotechar='"', fieldnames=fieldnames,
                                    quoting=csv.QUOTE_MINIMAL)

        csv_writer.writeheader()

        for idx, item in enumerate(data):

            if item[CompareList.seen]:
                checked = 1 if item[CompareList.flag_valid] else 0
            else:
                checked = -1

            db1 = db1_path_string  # self.compare1.db.as_posix()
            db2 = db2_path_string  # self.compare2.db.as_posix()
            # db = item[CompareList.db]
            nr_db1 = item[CompareList.nrs_db1]
            nr_db2 = item[CompareList.nrs_db2]

            id_single = -1
            id_single2 = -1
            image = -1
            image2 = -1
            valid = 0
            valid2 = 0
            idx_valid1 = 0
            idx_valid2 = 0
            obj_type = ''
            obj_type2 = ''
            group = -1
            group2 = -1

            data_c1 = {}
            data_c2 = {}
            data_env_c1 = {}
            data_env_c2 = {}

            certainty_c1 = 0
            certainty_c2 = 0

            c1_valids = [i for i, j in enumerate(item[CompareList.c1_valid]) if j == 1]
            c2_valids = [i for i, j in enumerate(item[CompareList.c2_valid]) if j == 1]

            for dum_data in [item[CompareList.c1_data][x] for x in c1_valids]:
                if dum_data:
                    if json.loads(dum_data).get('certainty', 'no') == 'yes':
                        certainty_c1 = 1
            for dum_data in [item[CompareList.c2_data][x] for x in c2_valids]:
                if dum_data:
                    if json.loads(dum_data).get('certainty', 'no') == 'yes':
                        certainty_c2 = 1

            if 1 in item[CompareList.c1_valid]:
                valid = 1
                idx_valid1 = item[CompareList.c1_valid].index(1)
            if 1 in item[CompareList.c2_valid]:
                valid2 = 1
                idx_valid2 = item[CompareList.c2_valid].index(1)

            if item[CompareList.c1_ids]:
                id_single = item[CompareList.c1_ids][idx_valid1]
                obj_type = item[CompareList.type][idx_valid1]
                image = item[CompareList.c1_image][idx_valid1]
                if item[CompareList.c1_data][idx_valid1]:
                    data_c1 = json.loads(item[CompareList.c1_data][idx_valid1])
                if item[CompareList.c1_data_env][idx_valid1]:
                    data_env_c1 = json.loads(item[CompareList.c1_data_env][idx_valid1])['data']
                if item[CompareList.c1_group][idx_valid1]:
                    group = item[CompareList.c1_group][idx_valid1]

            if item[CompareList.c2_ids]:
                id_single2 = item[CompareList.c2_ids][idx_valid2]
                obj_type2 = item[CompareList.type_other][idx_valid2]
                image2 = item[CompareList.c2_image][idx_valid2]
                if item[CompareList.c2_data][idx_valid2]:
                    data_c2 = json.loads(item[CompareList.c2_data][idx_valid2])
                if item[CompareList.c2_data_env][idx_valid2]:
                    data_env_c2 = json.loads(item[CompareList.c2_data_env][idx_valid2])['data']
                if item[CompareList.c2_group][idx_valid2]:
                    group2 = item[CompareList.c2_group][idx_valid2]

            # empty dict for that row
            row_dict = dict(zip(fieldnames, [None]*len(fieldnames)))

            # common
            row_dict['id'] = idx
            row_dict['db1_path'] = db1
            row_dict['db2_path'] = db2
            row_dict['inspected'] = checked
            row_dict['db1_nr_obj'] = nr_db1
            row_dict['db2_nr_obj'] = nr_db2

            # objects db 1
            # 'id_item_db1', 'valid_db1', 'id_image_db1', 'object_type_db1', 'id_resightset_db1'
            row_dict['db1_id_item'] = id_single
            row_dict['db1_valid'] = valid
            row_dict['db1_id_image'] = image
            row_dict['db1_object_type'] = obj_type
            row_dict['db1_certainty'] = certainty_c1
            row_dict['db1_id_resightset'] = group
            # data_c1, data_env_c1
            for key, value in data_c1.items():
                row_dict['db1_' + key] = value
            for key, value in data_env_c1.items():
                row_dict['db1_' + key] = value

            # objects db 2
            # 'id_item_db1', 'valid_db1', 'id_image_db1', 'object_type_db1', 'id_resightset_db1'
            row_dict['db2_id_item'] = id_single2
            row_dict['db2_valid'] = valid2
            row_dict['db2_id_image'] = image2
            row_dict['db2_object_type'] = obj_type2
            row_dict['db2_certainty'] = certainty_c2
            row_dict['db2_id_resightset'] = group2
            # data_c2, data_env_c2
            for key, value in data_c2.items():
                row_dict['db2_' + key] = value
            for key, value in data_env_c2.items():
                row_dict['db2_' + key] = value

            # Matching of data
            row_dict['match_objectType'] = 1 if obj_type2 == obj_type else 0
            row_dict['match_certainty'] = 1 if certainty_c2 == certainty_c1 else 0

            # Set everything first as no Match
            for value in header_match_data:
                row_dict[value] = 0

            for value in header_match_env_data:
                row_dict[value] = 0

            for key, value in data_c1.items():

                match_key = 'match_' + key
                row_dict[match_key] = 0

                if data_c2.get(key, False):
                    if data_c2[key] == value:
                        row_dict[match_key] = 1

            for key, value in data_env_c1.items():

                match_key = 'match_env_' + key
                row_dict[match_key] = 0

                if data_env_c2.get(key, False):
                    if data_env_c2[key] == value:
                        row_dict[match_key] = 1

            csv_writer.writerow(row_dict)
