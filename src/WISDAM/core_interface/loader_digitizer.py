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
from PySide6.QtCore import QPointF
from PySide6.QtGui import QPolygonF, QColor, QPainterPath

# from app.utils_qt import (create_tooltip_cropped_image, create_tooltip_objects)
from app.graphic.imageScene import ImageScene
from app.graphic.itemsGrahpicScene import PointAnnotation, PathAnnotation, PolygonAnnotation
from app.var_classes import look_up_attribute_db_column, ColorGui
from app.graphic.items_coloring import get_new_color_dict_objects

# WISDAM core
from db.dbHandler import DBHandler
from core_interface.wisdamIMAGE import WISDAMImage


def draw_geometry(scene: ImageScene, object_data, point_size: int, color: QColor):
    geom = json.loads(object_data['geom'])
    object_type = object_data['object_type']
    if geom['type'] == 'Point':
        new_item = PointAnnotation(color=color,
                                   projection=False,
                                   object_id=object_data['id'],
                                   image_id=object_data['image_id'],
                                   object_type=object_type,
                                   resight_set=object_data['resight_set'],
                                   group_area=object_data['group_area'],
                                   reviewed=object_data['reviewed'],
                                   source=object_data['source'])

        new_item.setRect(geom['coordinates'][0] - point_size / 2.0, geom['coordinates'][1] - point_size / 2.0,
                         point_size, point_size)
    elif geom['type'] == 'LineString':
        coordinates = geom['coordinates']

        path = QPainterPath(QPointF(*coordinates[0]))
        for coo in coordinates[1:]:
            path.lineTo(QPointF(*coo))

        new_item = PathAnnotation(color=color, projection=False,
                                  object_id=object_data['id'],
                                  image_id=object_data['image_id'],
                                  object_type=object_type,
                                  resight_set=object_data['resight_set'],
                                  group_area=object_data['group_area'],
                                  reviewed=object_data['reviewed'],
                                  source=object_data['source'])
        new_item.setPath(path)
    elif geom['type'] == 'Polygon':
        poly = geom['coordinates'][0]
        poly_image = QPolygonF([QPointF(*p) for p in poly])
        new_item = PolygonAnnotation(color=color, projection=False,
                                     object_id=object_data['id'],
                                     image_id=object_data['image_id'],
                                     object_type=object_type,
                                     resight_set=object_data['resight_set'],
                                     group_area=object_data['group_area'],
                                     reviewed=object_data['reviewed'],
                                     source=object_data['source'])
        new_item.setPolygon(QPolygonF(poly_image))

    else:
        return

    #new_item.setToolTip(create_tooltip_objects(object_data['image_id'],
    #                                           object_type,
    #                                           object_data['resight_set'],
    #                                           reviewed=object_data['reviewed'],
    #                                           source=object_data['source']))

    scene.addItem(new_item)


def draw_geometry_projections(scene: ImageScene,
                              image: WISDAMImage,
                              object_data,
                              point_size: int,
                              color: QColor):
    geom = json.loads(object_data['geom'])
    object_type = object_data['object_type']
    if geom['type'] == 'Point':

        p_pixel = image.image_model.project(np.array(geom['coordinates']))[0, :]
        if p_pixel is None:
            return

        new_item = PointAnnotation(color=color,
                                   projection=True,
                                   object_id=object_data['id'],
                                   image_id=object_data['image_id'],
                                   object_type=object_type,
                                   resight_set=object_data['resight_set'],
                                   reviewed=object_data['reviewed'],
                                   source=object_data['source'])

        new_item.setRect(p_pixel[0] - point_size / 2.0, p_pixel[1] - point_size / 2.0,
                         point_size, point_size)

    elif geom['type'] == 'LineString':
        coordinates = np.array(geom['coordinates'])

        result_projection = image.image_model.project(coordinates)
        if result_projection is None:
            return

        p_pixel, pixel_mask = result_projection
        path = QPainterPath(QPointF(*p_pixel[0]))
        for coo in p_pixel[1:]:
            path.lineTo(QPointF(*coo))

        new_item = PathAnnotation(color=color,
                                  projection=True,
                                  object_id=object_data['id'],
                                  image_id=object_data['image_id'],
                                  object_type=object_type,
                                  resight_set=object_data['resight_set'],
                                  reviewed=object_data['reviewed'],
                                  source=object_data['source'])
        new_item.setPath(path)

    elif geom['type'] == 'Polygon':

        poly = np.array(geom['coordinates'][0])

        result_projection = image.image_model.project(poly)
        if result_projection is None:
            return

        p_pixel, pixel_mask = result_projection
        poly_image = QPolygonF([QPointF(*point) for point in p_pixel])

        new_item = PolygonAnnotation(color=color,
                                     projection=True,
                                     object_id=object_data['id'],
                                     image_id=object_data['image_id'],
                                     object_type=object_type,
                                     resight_set=object_data['resight_set'],
                                     reviewed=object_data['reviewed'],
                                     source=object_data['source'])
        new_item.setPolygon(QPolygonF(poly_image))

    else:
        return

    #new_item.setToolTip(create_tooltip_cropped_image(object_data['image'],
    #                                                 object_data['image_id'],
    #                                                 object_type,
    #                                                 object_data['resight_set'],
    #                                                 reviewed=object_data['reviewed'],
    #                                                 source=object_data['source']))
    scene.addItem(new_item)


def loader_image_geom(db: DBHandler, scene: ImageScene, image: WISDAMImage, point_size: int,
                      color_attribute: str, default_dict: dict | None = None, default_value=None):
    # get color dict from db values with lookup table of attribute and DB column name
    color_attribute_db = look_up_attribute_db_column[color_attribute]

    if default_value is None:
        value_default = color_attribute_db['default']
    else:
        value_default = default_value

    # load geom from the image itself
    data_from_image = db.load_geometry(image.id)

    data_reprojection = []
    if image.is_geo_referenced:
        data_reprojection = db.load_geometry_overlap(image.id)

    if not (data_from_image or data_reprojection):
        return

    if color_attribute in default_dict.keys():
        color_dict = default_dict[color_attribute]

    else:

        color_values = []

        for single_object in data_from_image:
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                value = value_default
            if value not in color_values and value is not None:
                color_values.append(value)

        for single_object in data_reprojection:
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                value = value_default
            if value not in color_values and value is not None:
                color_values.append(value)

        color_values.sort()

        if default_value is not None:
            if default_value in color_values:
                color_values.insert(0, color_values.pop(color_values.index(default_value)))
            else:
                color_values.insert(0, default_value)

        color_dict = {'attribute': color_attribute, 'colors': get_new_color_dict_objects(color_values)}

    if data_from_image:
        for single_object in data_from_image:
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                value = value_default

            if value is not None:
                draw_geometry(scene, single_object, point_size,
                              color_dict['colors'].get(value, ColorGui.color_invalid_attribute_scenes))
            else:
                draw_geometry(scene, single_object, point_size, ColorGui.color_invalid_attribute_scenes)

    # load geom from other images

    if data_reprojection:
        for single_object in data_reprojection:
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                value = value_default
            if value is not None:
                draw_geometry_projections(scene, image, single_object, point_size,
                                          color_dict['colors'].get(value, ColorGui.color_invalid_attribute_scenes))
            else:
                draw_geometry_projections(scene, image, single_object, point_size,
                                          ColorGui.color_invalid_attribute_scenes)

    return color_dict
