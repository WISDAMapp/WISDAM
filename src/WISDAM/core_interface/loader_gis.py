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
import json
import numpy
from pathlib import Path
import time

from PySide6.QtGui import QPolygonF, QColor, QPainterPath
from PySide6.QtCore import QPointF

from app.graphic.itemsGrahpicScene import (PointAnnotation, PolygonAnnotation, PathAnnotation,
                                           PolygonFootprint, PointCenterpoint, PathImages, GISNode)
from app.graphic.gisScene import GISScene
from app.var_classes import (point_size_gis_standard, look_up_attribute_db_column, ColorGui)
from app.graphic.items_coloring import get_new_color_dict_objects, update_color_dict_objects
# from app.utils_qt import create_tooltip_cropped_image
from statistic.image_statistics import image_gsd_union_area_calculate

from db.dbHandler import DBHandler

logger = logging.getLogger(__name__)


def delay_qtimer():

    time.sleep(0.00001)


def draw_footprints(footprint, color, persistent_index):
    if footprint['geom']:
        poly = json.loads(footprint['geom'])
        poly_draw = QPolygonF()
        for p in poly['coordinates'][0]:
            p[1] = -p[1]
            poly_draw.append(QPointF(p[0], p[1]))
        item_footprint = PolygonFootprint(color=color,
                                          image_id=footprint['id'],
                                          group_image=footprint['group_image'],
                                          inspected=footprint['inspected'],
                                          flight_ref=footprint['flight_ref'],
                                          folder=Path(footprint['path']).parent.as_posix(),
                                          transect=footprint['transect'],
                                          block_id=footprint['block'])
        item_footprint.setPolygon(poly_draw)

        item_point = PointCenterpoint(color=color,
                                      image_id=footprint['id'],
                                      group_image=footprint['group_image'],
                                      inspected=footprint['inspected'],
                                      flight_ref=footprint['flight_ref'],
                                      folder=Path(footprint['path']).parent.as_posix(),
                                      transect=footprint['transect'],
                                      block_id=footprint['block'],
                                      persistent_index=persistent_index)

        item_point.setToolTip("ID: %i ; %s" % (footprint['id'], footprint['name']))

        item_point.setRect(footprint['x'] - point_size_gis_standard / 8.0,
                           -footprint['y'] - point_size_gis_standard / 8.0,
                           point_size_gis_standard / 4.0, point_size_gis_standard / 4.0)

        item_footprint.setParentItem(item_point)
        item_footprint.setVisible(False)

        # scene.addItem(item_point)

        return item_point
    return None


def draw_geom(geom_data, point_size: float, color_value):
    if geom_data['geom']:
        geom = json.loads(geom_data['geom'])
        object_type = geom_data['object_type']
        if geom['type'] == 'Point':

            new_item = PointAnnotation(color=color_value,
                                       projection=False,
                                       object_id=geom_data['id'],
                                       group_area=geom_data['group_area'],
                                       resight_set=geom_data['resight_set'],
                                       object_type=object_type,
                                       image_id=geom_data['image_id'],
                                       reviewed=geom_data['reviewed'],
                                       source=geom_data['source'],
                                       pen_width=0)
            new_item.setRect(geom['coordinates'][0] - point_size / 2.0, -geom['coordinates'][1] - point_size / 2.0,
                             point_size, point_size)

        elif geom['type'] == 'LineString':

            new_item = PathAnnotation(color=color_value,
                                      projection=False,
                                      object_id=geom_data['id'],
                                      resight_set=geom_data['resight_set'],
                                      group_area=geom_data['group_area'],
                                      object_type=object_type,
                                      image_id=geom_data['image_id'],
                                      reviewed=geom_data['reviewed'],
                                      source=geom_data['source'],
                                      pen_width=0,
                                      stroke_buffer=point_size_gis_standard / 2)

            path = QPainterPath(QPointF(geom['coordinates'][0][0], -geom['coordinates'][0][1]))
            for coo in geom['coordinates'][1:]:
                path.lineTo(QPointF(coo[0], -coo[1]))

            new_item.setPath(path)

        elif geom['type'] in ['Polygon', 'Rectangle']:

            new_item = PolygonAnnotation(color=color_value,
                                         projection=False,
                                         object_id=geom_data['id'],
                                         resight_set=geom_data['resight_set'],
                                         group_area=geom_data['group_area'],
                                         object_type=object_type,
                                         image_id=geom_data['image_id'],
                                         reviewed=geom_data['reviewed'],
                                         source=geom_data['source'],
                                         pen_width=0)
            poly_draw = QPolygonF()
            for p in geom['coordinates'][0]:
                p[1] = -p[1]
                poly_draw.append(QPointF(*p[0:2]))
            new_item.setPolygon(poly_draw)
        else:
            return

        #if geom_data['cropped_image']:
        #    new_item.setToolTip(create_tooltip_cropped_image(geom_data['cropped_image'],
        #                                                 geom_data['image_id'],
        #                                                 object_type,
        #                                                 geom_data['resight_set'],
        #                                                 reviewed=geom_data['reviewed'],
        #                                                 source=geom_data['source']))
        return new_item


def worker_heavy_loading(images, db_path, persistent_model_index, recalculate_area_gsd,
                         gis_color_attribute_objects, color_scheme):

    db = DBHandler.from_path(Path(db_path), '')
    gis_objects, node_list = loader_gis_geom_images_thread(db.path, persistent_index_dict=persistent_model_index)

    union_area, img_gsd = db.area_gsd

    if node_list:
        if images is None:
            images = db.load_images_list()
        if recalculate_area_gsd or union_area == 0.0 or union_area is None:
            union_area, img_gsd = image_gsd_union_area_calculate(images)
            db.set_area_gsd(union_area, img_gsd)

    geom_gis, color_dict_gis_objects = loader_gis_geom_objects(db.path,
                                                               color_attribute=gis_color_attribute_objects,
                                                               default_dict=color_scheme)

    return union_area, img_gsd, gis_objects, node_list, geom_gis, color_dict_gis_objects


def loader_gis_geom_images_thread(db_path,
                                  persistent_index_dict: dict | None = None, ):
    items_for_scene = []

    db = DBHandler.from_path(Path(db_path), '')
    footprints = db.load_images_gis()
    node_list: list[GISNode | None] = []
    if footprints:

        image_line_path: QPainterPath | None = None
        last_path = Path()
        for footprint in footprints:

            delay_qtimer()
            if Path(footprint['path']).parent != last_path:

                if image_line_path is not None:
                    path_line = PathImages()
                    path_line.setPath(image_line_path)
                    items_for_scene.append(path_line)
                    gis_node = GISNode()
                    pt_50 = image_line_path.pointAtPercent(0.5)
                    gis_node.setRect(pt_50.x() - 0.06, pt_50.y() - 0.06, 0.12, 0.12)

                    for idx_nodes, node in enumerate(node_list):
                        if node is not None:
                            if gis_node.collidesWithItem(node):
                                gis_node.setRect(node.boundingRect().united(gis_node.boundingRect()))
                                node_list[idx_nodes] = None
                    node_list.append(gis_node)

                    image_line_path = None

            last_path = Path(footprint['path']).parent
            if footprint['x'] is not None:

                if image_line_path is None:
                    image_line_path = QPainterPath(QPointF(footprint['x'], -footprint['y']))
                else:
                    current_point = QPointF(footprint['x'], -footprint['y'])
                    dist = current_point - image_line_path.pointAtPercent(1)

                    # Approx 100meter
                    if numpy.sqrt(dist.x() ** 2 + dist.y() ** 2) < 0.001:
                        image_line_path.lineTo(current_point)
                    else:
                        path_line = PathImages()
                        path_line.setPath(image_line_path)
                        items_for_scene.append(path_line)
                        gis_node = GISNode()
                        pt_50 = image_line_path.pointAtPercent(0.5)
                        gis_node.setRect(pt_50.x() - 0.06, pt_50.y() - 0.06, 0.12, 0.12)
                        for idx_nodes, node in enumerate(node_list):
                            if node is not None:
                                if gis_node.collidesWithItem(node):
                                    gis_node.setRect(node.boundingRect().united(gis_node.boundingRect()))
                                    node_list[idx_nodes] = None
                        node_list.append(gis_node)
                        image_line_path = QPainterPath(current_point)

            persistent_index = None
            if persistent_index_dict is not None:
                persistent_index = persistent_index_dict[Path(footprint['path']).as_posix()]
            items_for_scene.append(draw_footprints(footprint, QColor('black'), persistent_index))

        if image_line_path is not None:
            path_line = PathImages()
            path_line.setPath(image_line_path)
            items_for_scene.append(path_line)
            gis_node = GISNode()
            pt_50 = image_line_path.pointAtPercent(0.5)
            gis_node.setRect(pt_50.x() - 0.06, pt_50.y() - 0.06, 0.12, 0.12)

            for idx_nodes, node in enumerate(node_list):
                if node is not None:
                    if gis_node.collidesWithItem(node):
                        gis_node.setRect(node.boundingRect().united(gis_node.boundingRect()))
                        node_list[idx_nodes] = None
            node_list.append(gis_node)

    node_list = [x for x in node_list if x is not None]

    return items_for_scene, node_list


def loader_gis_geom_objects(db_path, color_attribute, default_dict: dict | None = None):

    db = DBHandler.from_path(Path(db_path), '')
    objects = db.load_objects_gis()
    color_dict = None

    geom_item_list = []
    if objects:

        color_attribute_db = look_up_attribute_db_column[color_attribute]

        if default_dict is not None:
            if color_attribute in default_dict.keys():
                color_dict = default_dict[color_attribute]

        if color_dict is None:
            color_values = []
            for single_object in objects:
                value = single_object[color_attribute_db['db_name']]
                if value is None:
                    value = color_attribute_db['default']

                if value not in color_values and value is not None:
                    color_values.append(value)

            color_dict = {'attribute': color_attribute, 'colors': get_new_color_dict_objects(color_values)}

        for single_object in objects:

            delay_qtimer()
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                value = color_attribute_db['default']

            if value is not None:
                # if the value would not be in the default dict than also print red
                # For future if default dicts are used more
                color = color_dict['colors'].get(value, ColorGui.color_invalid_attribute_scenes)
            else:
                color = ColorGui.color_invalid_attribute_scenes

            geom_item_list.append(draw_geom(single_object, point_size_gis_standard, color))

    return geom_item_list, color_dict


def loader_gis_geom_objects_single(db: DBHandler, scene: GISScene, object_id: int, color_dict: dict | None, attribute,
                                   default_dict: dict | None = None):
    """Add gis object to the GIS VIEW. Will use the current color regime in place"""

    single_object = db.load_objects_gis_single(object_id)
    if single_object:

        if color_dict is not None:

            color_attribute_db = look_up_attribute_db_column[color_dict['attribute']]
            value = single_object.get(color_attribute_db['db_name'], None)
            if value is None:
                # The value still can remain None if no default is wanted e.g. object type
                # Then later the object will be painted black but also None will not be stored in the color dict
                value = color_attribute_db['default']

        else:
            # No color dict, probably this is the first object which is added
            color_dict = {'attribute': attribute, 'colors': {}}
            color_attribute_db = look_up_attribute_db_column[attribute]
            value = single_object[color_attribute_db['db_name']]
            if value is None:
                # The value still can remain None if no default is wanted e.g. object type
                # Then later the object will be painted black but also None will not be stored in the color dict
                # update_color_dict_objects checks if value is None also
                value = color_attribute_db['default']

        color_dict, update = update_color_dict_objects(color_dict, value)
        # It could be possible that the value is still None, e.g. object type is not set jet
        if value is not None:
            color = color_dict['colors'].get(value, ColorGui.color_invalid_attribute_scenes)
        else:
            color = ColorGui.color_invalid_attribute_scenes
        item = draw_geom(single_object, point_size_gis_standard, color)
        if item is not None:
            scene.addItem(item)
        if update:
            color_dict = scene.color_objects(attribute=color_dict['attribute'], default_dict=default_dict)

        return color_dict
    return None
