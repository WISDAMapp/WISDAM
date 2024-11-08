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


import logging
from pathlib import Path
import json
import numpy as np
import csv

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


def row_list_json_extract(row: dict, header: list, json_keys_prefix: dict, geom_list: list | None = None) -> list:
    data = [''] * len(header)

    if geom_list is None:
        geom_list = []

    for key in row.keys():
        if key in header:
            data[header.index(key)] = str(row[key])

    for json_key, json_value in json_keys_prefix.items():
        if row[json_key]:
            json_data: dict = json.loads(json_value)
            for key, value in json_data.items():
                data[header.index(key)] = str(value)

    if len(geom_list) > 0:
        for epx_geom in geom_list:

            if row[epx_geom]:
                geo3d = json.loads(row[epx_geom])
                np_geo = np.array(geo3d['coordinates']).flatten()
                data[header.index(epx_geom)] = ' '.join([str(x) for x in np_geo])

    return data


def row_list_json_to_csv(row: dict, header: list) -> list:
    data = [''] * len(header)

    for key in row.keys():
        if key in header:
            data[header.index(key)] = str(row[key])

    return data


def sqlite_row_names(keys, exclude_list):
    header_list = []
    for element in keys:
        if element not in exclude_list:
            header_list.append(element)
    return header_list


def sqlite_row_names_json_extract(data, exclude_list, json_key_list, geom_key_list: list | None = None):
    if geom_key_list is None:
        geom_key_list = []

    header_list = sqlite_row_names(data[0].keys(), exclude_list + json_key_list)

    json_headers = []
    for row in data:

        for json_key in json_key_list:
            if row[json_key]:
                json_data = json.loads(row[json_key])
                for key in json_data.keys():
                    if key not in json_headers:
                        json_headers.append(key)

    return header_list + json_headers + geom_key_list


def export_footprints_csv(db: DBHandler, path_csv: Path | str) -> int:
    """Export image footprints as CSV File in utf-8
    :param db: DBHandler to use for export
    :param path_csv: The path to the csv to write. Will be replaced if exists
    :return: True, if success"""

    # if input is string instead of path
    path_csv = Path(path_csv)

    configuration: dict = json.loads(db.load_config()["configuration"])

    data = db.load_image_export()
    if data:

        # Get header with PRAGMA table_info(objects);
        header_standard = ["id", "user", "x", "y", "z", "flight_ref", "transect", "block", "group_image", "type",
                           "importer", "inspected",
                           "name", "path", "datetime", "width", "height", "math_model",
                           "area", "gsd", "tags"]

        meta_user = []
        meta_image = []
        for row in data:
            if row["meta_user"]:
                meta_user += ["meta_user: " + x for x in json.loads(row["meta_user"]).keys()]
            if row["meta_image"]:
                meta_image += ["meta_image: " + x for x in json.loads(row["meta_image"]).keys()]

        header = header_standard + list(set(meta_image))
        header += list(set(meta_user))

        env_header = ['environment_image: propagation'] + \
                     ['environment_image: ' + x for x in configuration['environment_data'].keys()]

        header += env_header
        header += ["geometry"]

        # CSV writer
        with open(path_csv.parent / (path_csv.stem + ".csv"), 'w', newline='', encoding='utf-8') as fid:

            csv_writer = csv.writer(fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow(header)

            for row in data:
                csv_row = [''] * len(header)

                for element_single in header_standard:
                    if row[element_single] is not None:
                        csv_row[header.index(element_single)] = row[element_single]

                if row["meta_user"]:
                    for key, value in json.loads(row["meta_user"]).items():
                        csv_row[header.index("meta_user: " + key)] = value

                if row["meta_image"]:
                    for key, value in json.loads(row["meta_image"]).items():
                        csv_row[header.index("meta_image: " + key)] = value

                if row["data_env"]:
                    csv_row[header.index('environment_image: propagation')] = json.loads(row['data_env'])['propagation']
                    for key, value in json.loads(row['data_env'])['data'].items():
                        csv_row[header.index("environment_image: " + key)] = value

                if row['geom']:
                    csv_row[header.index('geometry')] = row['geom']

                csv_writer.writerow(csv_row)

        return len(data)

    return 0


def export_objects_csv(db: DBHandler, path_csv: Path | str, flag_first_certain: bool = False) -> int:
    """Export objects as CSV File in utf-8
    :param db: DBHandler to use for export
    :param path_csv: The path to the csv to write. Will be replaced if exists
    :param flag_first_certain: Flag, if only first certain should be exported
    :return: True if success"""

    # if input is string instead of path
    path_csv = Path(path_csv)

    configuration: dict = json.loads(db.load_config()["configuration"])

    data = db.obj_load_all(flag_first_certain=flag_first_certain)

    if data:

        # Get header with PRAGMA table_info(objects) and look at db load_all for extra columns;
        header_standard = ["id", "image", "image_name", "img_path", "group_image", "transect", "block", "datetime",
                           "user", "active", "source", "reviewed", "area", "gsd", "resight_set", "resight_set",
                           "object_type", "meta_type", "highlighted", "tags"]

        meta_data = []
        for row in data:
            if row["data"]:
                meta_data += ["meta_data: " + x for x in json.loads(row["data"]).keys()]

        header = header_standard + list(set(meta_data))

        env_header = ['environment_image: propagation'] + \
                     ['environment_image: ' + x for x in configuration['environment_data'].keys()]

        header += env_header

        env_header = ['environment_object: propagation'] + \
                     ['environment_object: ' + x for x in configuration['environment_data'].keys()]

        header += env_header

        header += ["geometry2d"]
        header += ["geometry3d"]

        # CSV writer
        with open(path_csv.parent / (path_csv.stem + ".csv"), 'w', newline='', encoding='utf-8') as fid:

            csv_writer = csv.writer(fid, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

            csv_writer.writerow(header)

            for row in data:
                csv_row = [''] * len(header)

                for element_single in header_standard:
                    if row[element_single] is not None:
                        csv_row[header.index(element_single)] = row[element_single]

                if row["data"]:
                    for key, value in json.loads(row["data"]).items():
                        csv_row[header.index("meta_data: " + key)] = value

                if row["image_data_env"]:
                    csv_row[header.index('environment_image: propagation')] = \
                        json.loads(row['image_data_env'])['propagation']
                    for key, value in json.loads(row['image_data_env'])['data'].items():
                        csv_row[header.index("environment_image: " + key)] = value

                if row["data_env"]:
                    csv_row[header.index('environment_object: propagation')] = \
                        json.loads(row['data_env'])['propagation']
                    for key, value in json.loads(row['data_env'])['data'].items():
                        csv_row[header.index("environment_object: " + key)] = value

                if row['geo2d']:
                    csv_row[header.index('geometry2d')] = row['geo2d']

                if row['geo']:
                    csv_row[header.index('geometry3d')] = row['geo']

                csv_writer.writerow(csv_row)

        return len(data)

    return 0


