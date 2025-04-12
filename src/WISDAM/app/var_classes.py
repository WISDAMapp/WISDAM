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


from enum import IntEnum
import logging

import shapely.errors
from PySide6.QtGui import QColor, QBrush
from PySide6.QtCore import Qt
from shapely import Geometry, Polygon, Point, LineString
from shapely import geometry
import numpy as np


license_version = "GNU General Public License v3 or later (GPLv3+)"
build_year = "2025"

url_wisdam = "https://wisdamapp.org"

# Attributes for the icon view of thumbnails and AI
spacing_grid = 10
icon_margin = 3
icon_footer_padding = 14
text_margin = 8


zoomin_factor = 0.8
point_size = 10

point_size_gis_standard = 0.0002

object_name_file_header = "# First entry is object main name (e.g. TAXA); followed by object sub names (e.g. Species)\n"
object_name_file_header += "# If you want to have standard empty as first sub item add ;; (empty sub name)\n"

look_up_attribute_db_column = {'source': {'db_name': 'source', 'default': 0},
                               'projection': {'db_name': 'projection', 'default': 0},
                               'object_type': {'db_name': 'object_type', 'default': None},
                               'resight_set': {'db_name': 'resight_set', 'default': 0},
                               'group_area': {'db_name': 'group_area', 'default': 0},
                               'reviewed': {'db_name': 'reviewed', 'default': 0},
                               'image_id': {'db_name': 'image_id', 'default': 0},
                               'inspected': {'db_name': 'inspected', 'default': 0},
                               'folder': {'db_name': 'folder', 'default': None},
                               'flight_ref': {'db_name': 'flight_ref', 'default': None},
                               'block': {'db_name': 'block', 'default': None},
                               'transect': {'db_name': 'transect', 'default': None},
                               'group_image': {'db_name': 'group_image', 'default': 0}}


# Color Definitions
class ColorGui:
    color_invalid_attribute_scenes = QColor('black')

    brush_dark_red = QBrush(QColor(103, 40, 23))
    brush_dark_green = QBrush(QColor(0, 113, 77))
    brush_light_green = QBrush(QColor('#476647'))

    color_dark_red = QColor(103, 40, 23)
    color_dark_green = QColor(0, 113, 77)
    color_mid_yellow = QColor(102, 102, 0)
    color_mid_blue = QColor(0, 66, 100)

    color_overlay = QColor(255, 255, 0, 50)
    color_overlay_hoover = QColor(0, 255, 0, 50)

    color_on_image_normal = QColor(255, 0, 0, 50)
    color_on_image_hoover = QColor(0, 255, 0, 50)

    color_on_image_selected_gis = QColor(255, 0, 0, 50)
    color_on_image_normal_gis = QColor(255, 165, 0, 50)
    c_on_image_normal_gis = (255, 165, 0, 50)

    color_inspected = QBrush(QColor(130, 110, 30))
    color_no_georef = QBrush(QColor(0, 77, 113))
    color_georef = QBrush(QColor(0, 113, 77))
    color_no_path = QBrush(QColor(103, 40, 23))
    color_ortho = QColor(0, 66, 100)
    color_extension = QColor(232, 145, 14)
    color_object = QColor(40, 44, 52)
    color_source = QColor(3, 128, 73)

    color_not_active = QColor("#85230b")
    color_active = QColor("#23e620")
    color_selection = QColor("#0ebee6")
    color_imported = QColor("#0ebee6")
    color_scheme_start = {"projection": {"attribute": "projection", "colors": {0: "#96ffaa00", 1: "#96ff007f"}},
                          "reviewed": {"attribute": "reviewed", "colors": {0: "#fa6000", 1: "#53fa00"}},
                          "inspected": {"attribute": "inspected", "colors": {0: "#fa6000", 1: "#53fa00"}}}

    # For Meta Popup and Main image it should be the same name
    color_env_none = "background-color: transparent;border-radius: 15px;"
    color_env_propagate = "background-color: rgba(127, 84, 0,122);border-radius: 15px;"
    color_env_object = "background-color: rgba(0, 50, 72,122);border-radius: 15px;"
    color_env_object_propagate = "background-color: rgba(61, 46, 87,122);border-radius: 15px;"
    color_env_db = "background-color: rgba(72, 100, 92,122);border-radius: 15px;"

    color_gauge_img_inspected_progress = QColor(85, 170, 255)
    color_gauge_img_inspected_inner = QColor(58, 58, 107)
    color_gauge_img_inspected_outer = QColor(85, 85, 127, 100)

    color_gauge_img_georef_percent = QColor(85, 255, 107)
    color_gauge_img_georef_inner = QColor(58, 107, 58)
    color_gauge_img_georef_outer = QColor(85, 127, 58, 100)

    color_gauge_ai_reviewed_percent = QColor(255, 170, 85)
    color_gauge_ai_reviewed_inner = QColor(107, 58, 58)
    color_gauge_ai_reviewed_outer = QColor(127, 85, 85, 100)

    color_gauge_ai_imported_percent = QColor(170, 107, 200)
    color_gauge_ai_imported_inner = QColor(60, 30, 50)
    color_gauge_ai_imported_outer = QColor(85, 58, 100, 100)


logging_style = {
    logging.DEBUG: {'txt': 'white', 'frame': "background-color: rgba(34, 113, 150, 190);",
                    'icon': u":/icons/icons/info-40.svg"},
    logging.INFO: {'txt': 'white', 'frame': "background-color: rgba(34, 113, 150, 190);",
                   'icon': u":/icons/icons/info-40.svg"},
    logging.WARNING: {'txt': 'orange', 'frame': "background-color: rgb(150, 146, 34);",
                      'icon': u":/icons/icons/warning-40.svg"},
    logging.ERROR: {'txt': QColor('#f3523a'), 'frame': "background-color: rgba(130, 67, 34, 190);",
                    'icon': u":/icons/icons/error-40.svg"},
    logging.CRITICAL: {'txt': 'purple', 'frame': "background-color: rgba(128, 0, 128, 190);",
                       'icon': u":/icons/icons/error-40.svg"},

    # extra level by extra mapping of info
    # should not be used if error or critical is the current info displayed
    "finished": {'txt': 'green', 'frame': "background-color: rgba(92, 150, 135, 190);",
                 'icon': u":/icons/icons/flat_tick_icon.svg"}
}

gis_node_pixmap = u":/icons/icons/pin.svg"


def delimiter_switch(argument):
    switcher = {
        "Space": " ",
        "Comma": ",",
        "Semi-Colon": ";",
        "Tabulator": "\t",
    }
    return switcher.get(argument, " ")


class GalleryIconSize:
    width = 250
    height = 250


class AISize:
    width = 250
    height = 250


class NavRect:
    width = 100
    height = 90


class ObjectSourceList:
    manual = 0
    ai = 1
    external = 2


def source_switch(argument):
    switcher = {
        0: "manual",
        1: "ai",
        2: "external",
    }
    return switcher.get(argument, "invalid")


def review_switch(argument):
    switcher = {
        0: "no",
        1: "yes",
    }
    return switcher.get(argument, "invalid")


image_list_header = ['Name', 'id', 'Insp.', 'Objs.', 'Geo', 'Type', 'Imp.', 'GSD [cm]', 'Area [m²]', 'Path', 'active']
image_list_folder_dummy = ['', '', 0, 0, '', '', '', 0.0, 0.0, 'Path', False]


class ImageList:
    name = 0
    id = 1
    inspected = 2
    nr_sightings = 3
    georef = 4
    ortho = 5
    importers = 6
    gsd = 7
    area = 8

    # For the model view it is important to have the non-visible in the end otherwise index will change of the row
    path = 9
    # active is only for visualization- means that this is the current image activated
    active = 10
    path_exists = 11


class WISDAMObject:

    def __init__(self):
        self.id = 0
        self.type = ''
        self.geom_type = ''
        self.meta = {}


group_area_header = ['Id', 'Nr. Sightings', 'Types', 'position']


class GroupAreaList:
    id = 0
    nr_sightings = 1
    object_type = 2
    position = 3


class GalleryData:
    def __init__(self):
        self.id = 0
        self.image = 0
        self.active = 0
        self.image_type = 0
        self.source = 0
        self.extension = 'JPG'
        self.object_type = 'none'
        self.group_area = 0
        self.resight_set = 0
        self.thumbnail = None
        self.tags = {}
        self.highlighted = 0
        self.folder = ""
        self.reviewed = 0


class GalleryRoles(IntEnum):
    id = Qt.UserRole + 1
    type = Qt.UserRole + 2
    object_type = Qt.UserRole + 3
    source = Qt.UserRole + 4

    image = Qt.UserRole + 5
    image_type = Qt.UserRole + 6
    extension = Qt.UserRole + 7
    folder = Qt.UserRole + 8
    filename = Qt.UserRole + 9

    group_area = Qt.UserRole + 10
    resight_set = Qt.UserRole + 11

    active = Qt.UserRole + 12
    thumbnail = Qt.UserRole + 13
    tags = Qt.UserRole + 14
    highlighted = Qt.UserRole + 15
    reviewed = Qt.UserRole + 16


class AIData:
    id = 0
    object_type = 'none'
    active = 0
    probability = 0
    ai_run = 0
    imported = 0
    thumbnail = None
    image_id = 0


class AiRoles(IntEnum):
    id = Qt.UserRole + 1
    object_type = Qt.UserRole + 2
    active = Qt.UserRole + 3
    probability = Qt.UserRole + 4
    ai_run = Qt.UserRole + 5
    imported = Qt.UserRole + 6
    thumbnail = Qt.UserRole + 7
    image_id = Qt.UserRole + 8


class Instructions(IntEnum):
    No_Instruction = 0
    Point_Instruction = 1
    LineString_Instruction = 2
    Rectangle_Instruction = 3
    Polygon_Instruction = 4


class Selection(IntEnum):
    Rectangle = 0
    Lasso = 1
    Brush = 2
    Polygon = 3


class ExternalSighting:
    name = ''
    img = ''
    geometry = ''
    geom_type = ''
    object_type = ''
    meta_data = ''
    env_data = ''


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False


def external_surety(argument):
    switcher = {
        "certain": 0,
        "probable": 1,
        "guess": 2,
    }
    return switcher.get(argument, 0)


def geometry_to_np_array(geom: Geometry | Polygon | Point | LineString) -> np.ndarray:

    if geom.geom_type == 'Point':

        return np.array(geom.coords)

    elif geom.geom_type == 'LineString':
        return np.array(geom.coords)

    elif geom.geom_type == 'Polygon':

        return np.array(geom.exterior.coords)


def np_array_to_geom(points: np.ndarray, geom_type: str) -> Point | Polygon | LineString:

    if geom_type not in ['Point', 'LineString', 'Polygon']:
        raise ValueError(r"Geometry is not supported. Only 'Point', 'LineString', 'Polygon'")

    try:

        if geom_type == 'Point':
            geom = geometry.Point(points)
        elif geom_type == 'LineString':
            geom = geometry.LineString(points)
        elif geom_type == 'Polygon':
            geom = geometry.Polygon(points)
        else:
            raise ValueError(r"Geometry is not supported. Only 'Point', 'LineString', 'Polygon'")

        return geom
    except shapely.errors.GEOSException | ValueError as e:
        raise ValueError("Geometry creation failed") from e
