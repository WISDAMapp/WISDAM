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

from collections import defaultdict
import logging
from pathlib import Path
import json
from shapely import geometry

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


def is_numeric(s):
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def is_json(s):
    try:
        # A string integer, float and single string are valid jsons.
        # So we need to check if the parsed string has keys or is instance dict
        loaded_dict = json.loads(s)
        # Test if that thing has a key
        # alternatively we could check isinstance
        _ = loaded_dict.keys()
        return loaded_dict
    except (ValueError, TypeError, AttributeError):
        return None


def format_test(value):
    ret_value = is_numeric(value)
    if ret_value is not None:
        if ret_value.is_integer():
            return 'int'
        else:
            return 'float'
    else:
        # string, sub json and all other
        return 'str'


def choose_format(values) -> str:

    if "str" in values:
        return "str"
    elif "int" in values:
        return "int"
    elif "float" in values:
        return"float"
    else:
        return "str"


def format_values(value, format_value: str):
    if format_value == "int":
        return int(value)
    elif format_value == "float":
        return float(value)
    else:
        return str(value)


def get_field_types(data, keys_wanted: list, env_obj: str | None = None, env_image: str | None = None) \
        -> tuple[dict, dict, dict]:
    """get field types for all rows and decide which one to use using a lookup"""
    field_types = defaultdict(set)
    env_obj_types = defaultdict(set)
    env_image_types = defaultdict(set)
    for rows in data:

        for db_key, db_value in rows.items():
            if db_key in keys_wanted:
                if db_value is not None:

                    value_json = is_json(db_value)
                    if value_json is not None:
                        for k, v in value_json.items():

                            # SUB json of json will be formatted as string
                            field_types[k].add(format_test(v))

                    else:
                        field_types[db_key].add(format_test(db_value))

        if env_obj is not None:
            if rows[env_obj]:
                data_env = json.loads(rows[env_obj])
                for k, v in data_env['data'].items():
                    env_obj_types[k].add(format_test(v))

        if env_image is not None:
            if rows[env_image]:
                data_env_image = json.loads(rows[env_image])
                for k, v in data_env_image['data'].items():
                    env_image_types[k].add(format_test(v))

    field_types_export = {}
    for key, formats_value in field_types.items():

        field_types_export[key] = choose_format(formats_value)

    env_obj_types_export = {}
    for key, formats_value in env_obj_types.items():
        env_obj_types_export[key] = choose_format(formats_value)

    env_image_types_export = {}
    for key, formats_value in env_image_types.items():
        env_image_types_export[key] = choose_format(formats_value)

    return field_types_export, env_obj_types_export, env_image_types_export


def export_objects_json(db: DBHandler, path_json: Path | str,
                        flag_first_certain: bool = False,
                        dict_return_only=False) -> tuple[int, dict]:
    """Export objects as JSON File in utf-8
    :param db: DBHandler to use for export
    :param path_json: The path to the json to write. Will be replaced if exists
    :param flag_first_certain: Flag, if only first certain should be exported
    :param dict_return_only: Only return geojson dictionary and do not write the geojson file.
                             Used to export other formats with geopandas.
    :return: True if success"""

    # if input is string instead of path
    path_json = Path(path_json)

    data = db.obj_load_all(flag_first_certain=flag_first_certain)
    json_dict = {}
    if data:

        json_dict['type'] = 'FeatureCollection'
        json_dict['name'] = path_json.stem
        json_dict['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}

        exclude_list = ['image_path', 'geom3d', 'geom2d', 'geo', 'data_env', 'image_data_env',
                        'geo2d', 'cropped_image']

        keys_wanted = [val for val in data[0].keys() if val not in exclude_list]

        json_dict_features = []

        field_types, env_obj_types, env_img_types = get_field_types(data,
                                                                    keys_wanted=keys_wanted,
                                                                    env_obj='data_env',
                                                                    env_image='image_data_env')

        for rows in data:

            feature_dict = {'type': 'Feature'}
            prop_dict = {}

            for db_key, db_value in rows.items():
                if db_key in keys_wanted:
                    if db_value is not None:

                        # Test if the value is a dictionary itself
                        value_json = is_json(db_value)
                        if value_json is not None:
                            for k, v in value_json.items():
                                prop_dict[k] = format_values(v, field_types[k])
                        else:
                            prop_dict[db_key] = format_values(db_value, field_types[db_key])

            if rows['data_env']:
                data_env = json.loads(rows['data_env'])
                prop_dict['environment_object_propagation'] = format_values(data_env['propagation'], 'int')
                for k, v in data_env['data'].items():
                    prop_dict['environment_object_' + k] = format_values(v, env_obj_types[k])

            if rows['image_data_env']:
                data_env = json.loads(rows['image_data_env'])
                prop_dict['environment_image_propagation'] = format_values(data_env['propagation'], 'int')
                for k, v in data_env['data'].items():
                    prop_dict['environment_image_' + k] = format_values(v, env_img_types[k])

            feature_dict['properties'] = prop_dict

            feature_dict['geometry'] = {}
            if rows['geo']:
                feature_dict['geometry'] = json.loads(rows['geo'])

            json_dict_features.append(feature_dict)

        json_dict['features'] = json_dict_features

        if not dict_return_only:
            with open(path_json, 'w', encoding='utf8') as json_file:
                json.dump(json_dict, json_file, ensure_ascii=False, indent=2)

            return len(data), {}

        return len(data), json_dict

    return 0, {}


def export_objects_as_point_json(db: DBHandler, path_json: Path | str,
                                 flag_first_certain: bool = False,
                                 dict_return_only=False) -> tuple[int, dict]:
    """Export objects as points(center point) as JSON File in utf-8
    :param db: DBHandler to use for export
    :param path_json: The path to the json to write. Will be replaced if exists
    :param flag_first_certain: Flag, if only first certain should be exported
    :param dict_return_only: Only return geojson dictionary and do not write the geojson file.
                             Used to export other formats with geopandas
    :return: True if success"""

    # if input is string instead of path
    path_json = Path(path_json)

    data = db.obj_load_all(flag_first_certain=flag_first_certain)
    json_dict = {}
    if data:

        json_dict['type'] = 'FeatureCollection'
        json_dict['name'] = path_json.stem
        json_dict['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}

        exclude_list = ['img_path', 'data_env', 'image_data_env', 'geom3d', 'geom2d', 'geo', 'geo2d', 'cropped_image']
        keys_wanted = [val for val in data[0].keys() if val not in exclude_list]
        json_dict_features = []

        field_types, env_obj_types, env_img_types = get_field_types(data,
                                                                    keys_wanted=keys_wanted,
                                                                    env_obj='data_env',
                                                                    env_image='image_data_env')

        for rows in data:

            feature_dict = {'type': 'Feature'}
            prop_dict = {}

            for db_key, db_value in rows.items():
                if db_key in keys_wanted:
                    if db_value is not None:

                        # Test if the value is a dictionary itself
                        value_json = is_json(db_value)
                        if value_json is not None:
                            for k, v in value_json.items():
                                prop_dict[k] = format_values(v, field_types[k])
                        else:
                            prop_dict[db_key] = format_values(db_value, field_types[db_key])

            if rows['data_env']:
                data_env = json.loads(rows['data_env'])
                prop_dict['environment_object_propagation'] = format_values(data_env['propagation'], 'int')
                for k, v in data_env['data'].items():
                    prop_dict['environment_object_' + k] = format_values(v, env_obj_types[k])

            if rows['image_data_env']:
                data_env = json.loads(rows['image_data_env'])
                prop_dict['environment_image_propagation'] = format_values(data_env['propagation'], 'int')
                for k, v in data_env['data'].items():
                    prop_dict['environment_image_' + k] = format_values(v, env_img_types[k])

            feature_dict['properties'] = prop_dict

            feature_dict['geometry'] = {}
            if rows['geo']:
                # Centroid of geometry will be stored as geojson geometry
                geom = geometry.shape(json.loads(rows['geo']))
                feature_dict['geometry'] = geometry.mapping(geom.centroid)

            json_dict_features.append(feature_dict)

        json_dict['features'] = json_dict_features

        if not dict_return_only:
            with open(path_json, 'w', encoding='utf8') as json_file:
                json.dump(json_dict, json_file, ensure_ascii=False, indent=2)

            return len(json_dict["features"]), {}
        return len(json_dict["features"]), json_dict

    return 0, {}


def export_footprints_json(db: DBHandler, path_json: Path | str, dict_return_only=False) -> tuple[int, dict]:
    """Export image footprints as JSON File in utf-8
    :param db: DBHandler to use for export
    :param path_json: The path to the json to write. Will be replaced if exists
    :param dict_return_only: Only return geojson dictionary and do not write the geojson file.
                             Used to export other formats with geopandas
    :return: True, if export is success"""

    # if input is string instead of path
    path_json = Path(path_json)

    data = db.load_image_export()
    json_dict = {}
    if data:

        json_dict['type'] = 'FeatureCollection'
        json_dict['name'] = path_json.stem
        json_dict['crs'] = {"type": "name", "properties": {"name": "urn:ogc:def:crs:OGC:1.3:CRS84"}}

        exclude_list = ['position', 'centerpoint', 'footprint', 'geom', 'orientation_matrix'
                                                                        'width', 'height', 'data_env']

        keys_wanted = [val for val in data[0].keys() if val not in exclude_list]
        json_dict_features = []

        field_types, env_obj_types, env_img_types = get_field_types(data,
                                                                    keys_wanted=keys_wanted,
                                                                    env_obj=None,
                                                                    env_image='data_env')

        for rows in data:

            feature_dict = {'type': 'Feature'}

            prop_dict = {}
            for db_key, db_value in rows.items():
                if db_key in keys_wanted:
                    if db_value is not None:

                        # Test if the value is a dictionary itself
                        value_json = is_json(db_value)
                        if value_json is not None:
                            for k, v in value_json.items():
                                prop_dict[k] = format_values(v, field_types[k])
                        else:
                            prop_dict[db_key] = format_values(db_value, field_types[db_key])

            if rows['data_env']:
                data_env = json.loads(rows['data_env'])
                prop_dict['environment_image_propagation'] = format_values(data_env['propagation'], 'int')
                for k, v in data_env['data'].items():
                    prop_dict['environment_image_' + k] = format_values(v, env_img_types[k])

            feature_dict['properties'] = prop_dict

            feature_dict['geometry'] = {}
            if rows['geom']:
                feature_dict['geometry'] = json.loads(rows['geom'])

            json_dict_features.append(feature_dict)

        json_dict['features'] = json_dict_features

        # Save json
        if not dict_return_only:
            with open(path_json, 'w', encoding='utf8') as json_file:
                json.dump(json_dict, json_file, ensure_ascii=False, indent=2)

            # Noo dict return needed, save time for exit
            return len(json_dict["features"]), {}

        return len(json_dict["features"]), json_dict

    return 0, {}
