# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2026 Martin Wieser.
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
from pyproj import CRS

from PySide6.QtCore import QPointF, QRectF
from PySide6.QtGui import QPolygonF, QColor, QPainterPath

# from app.utils_qt import (create_tooltip_cropped_image, create_tooltip_objects)
from app.graphic.imageScene import ImageScene
from app.graphic.itemsGrahpicScene import (
    RectangleAnnotation,
    PointAnnotation,
    PathAnnotation,
    PolygonAnnotation,
)
from app.var_classes import look_up_attribute_db_column, ColorGui
from app.graphic.items_coloring import get_new_color_dict_objects

# WISDAM core
from db.dbHandler import DBHandler
from core_interface.wisdamIMAGE import WISDAMImage

from weitsicht.exceptions import WeitsichtError


def _unique_values(values: list[float], tolerance: float = 1e-6) -> list[float]:
    unique = []
    for value in values:
        if not any(abs(value - current) <= tolerance for current in unique):
            unique.append(value)
    return unique


def _point_matches(point: QPointF, x: float, y: float, tolerance: float = 1e-6) -> bool:
    return abs(point.x() - x) <= tolerance and abs(point.y() - y) <= tolerance


def rectangle_from_polygon(poly: list) -> QRectF | None:
    points = [QPointF(*p) for p in poly]
    if len(points) > 1 and _point_matches(points[0], points[-1].x(), points[-1].y()):
        points = points[:-1]

    if len(points) != 4:
        return None

    x_values = _unique_values([point.x() for point in points])
    y_values = _unique_values([point.y() for point in points])
    if len(x_values) != 2 or len(y_values) != 2:
        return None

    min_x, max_x = min(x_values), max(x_values)
    min_y, max_y = min(y_values), max(y_values)
    if abs(max_x - min_x) <= 1e-6 or abs(max_y - min_y) <= 1e-6:
        return None

    corners = [(min_x, min_y), (max_x, min_y), (max_x, max_y), (min_x, max_y)]
    if not all(
        any(_point_matches(point, x, y) for point in points) for x, y in corners
    ):
        return None

    return QRectF(QPointF(min_x, min_y), QPointF(max_x, max_y)).normalized()


def draw_geometry(scene: ImageScene, object_data, point_size: int, color: QColor):
    geom = json.loads(object_data["geom"])
    object_type = object_data["object_type"]
    if geom["type"] == "Point":
        new_item = PointAnnotation(
            color=color,
            projection=False,
            object_id=object_data["id"],
            image_id=object_data["image_id"],
            object_type=object_type,
            resight_set=object_data["resight_set"],
            group_area=object_data["group_area"],
            reviewed=object_data["reviewed"],
            source=object_data["source"],
        )

        new_item.setRect(
            geom["coordinates"][0] - point_size / 2.0,
            geom["coordinates"][1] - point_size / 2.0,
            point_size,
            point_size,
        )
    elif geom["type"] == "LineString":
        coordinates = geom["coordinates"]

        path = QPainterPath(QPointF(*coordinates[0]))
        for coo in coordinates[1:]:
            path.lineTo(QPointF(*coo))

        new_item = PathAnnotation(
            color=color,
            projection=False,
            object_id=object_data["id"],
            image_id=object_data["image_id"],
            object_type=object_type,
            resight_set=object_data["resight_set"],
            group_area=object_data["group_area"],
            reviewed=object_data["reviewed"],
            source=object_data["source"],
        )
        new_item.setPath(path)
    elif geom["type"] == "Polygon":
        poly = geom["coordinates"][0]
        rect = rectangle_from_polygon(poly)
        if rect is not None:
            new_item = RectangleAnnotation(
                color=color,
                projection=False,
                object_id=object_data["id"],
                image_id=object_data["image_id"],
                object_type=object_type,
                resight_set=object_data["resight_set"],
                group_area=object_data["group_area"],
                reviewed=object_data["reviewed"],
                source=object_data["source"],
            )
            new_item.setRect(rect)
        else:
            poly_image = QPolygonF([QPointF(*p) for p in poly])
            new_item = PolygonAnnotation(
                color=color,
                projection=False,
                object_id=object_data["id"],
                image_id=object_data["image_id"],
                object_type=object_type,
                resight_set=object_data["resight_set"],
                group_area=object_data["group_area"],
                reviewed=object_data["reviewed"],
                source=object_data["source"],
            )
            new_item.setPolygon(QPolygonF(poly_image))

    else:
        return

    # new_item.setToolTip(create_tooltip_objects(object_data['image_id'],
    #                                           object_type,
    #                                           object_data['resight_set'],
    #                                           reviewed=object_data['reviewed'],
    #                                           source=object_data['source']))

    scene.addItem(new_item)


def draw_geometry_projections(
    scene: ImageScene, image: WISDAMImage, object_data, point_size: int, color: QColor
):
    geom = json.loads(object_data["geom"])
    object_type = object_data["object_type"]
    if geom["type"] == "Point":
        coordinates = np.asarray(geom["coordinates"])
        if coordinates.ndim == 1:
            coordinates = np.array([coordinates])

        try:
            result_projection = image.image_model.project(coordinates, crs_s=CRS(4979))
        except (WeitsichtError, ValueError, TypeError):
            return

        if result_projection is None or not result_projection.ok:
            return
        p_pixel = np.asarray(result_projection.pixels)
        if p_pixel.size == 0:
            return

        new_item = PointAnnotation(
            color=color,
            projection=True,
            object_id=object_data["id"],
            image_id=object_data["image_id"],
            image_datetime=object_data["image_datetime"],
            object_type=object_type,
            resight_set=object_data["resight_set"],
            reviewed=object_data["reviewed"],
            source=object_data["source"],
        )

        new_item.setRect(
            p_pixel[0][0] - point_size / 2.0,
            p_pixel[0][1] - point_size / 2.0,
            point_size,
            point_size,
        )

    elif geom["type"] == "LineString":
        coordinates = np.array(geom["coordinates"])

        try:
            result_projection = image.image_model.project(coordinates, crs_s=CRS(4979))
        except (WeitsichtError, ValueError, TypeError):
            return

        if result_projection is None or not result_projection.ok:
            return

        p_pixel = np.asarray(result_projection.pixels)
        if p_pixel.shape[0] < 2:
            return

        path = QPainterPath(QPointF(*p_pixel[0]))
        for coo in p_pixel[1:]:
            path.lineTo(QPointF(*coo))

        new_item = PathAnnotation(
            color=color,
            projection=True,
            object_id=object_data["id"],
            image_id=object_data["image_id"],
            image_datetime=object_data["image_datetime"],
            object_type=object_type,
            resight_set=object_data["resight_set"],
            reviewed=object_data["reviewed"],
            source=object_data["source"],
        )
        new_item.setPath(path)

    elif geom["type"] == "Polygon":
        poly = np.array(geom["coordinates"][0])

        try:
            result_projection = image.image_model.project(poly, crs_s=CRS(4979))
        except (WeitsichtError, ValueError, TypeError):
            return

        if result_projection is None or not result_projection.ok:
            return

        p_pixel = np.asarray(result_projection.pixels)
        if p_pixel.shape[0] < 3:
            return

        poly_image = QPolygonF([QPointF(*point) for point in p_pixel])

        new_item = PolygonAnnotation(
            color=color,
            projection=True,
            object_id=object_data["id"],
            image_id=object_data["image_id"],
            image_datetime=object_data["image_datetime"],
            object_type=object_type,
            resight_set=object_data["resight_set"],
            reviewed=object_data["reviewed"],
            source=object_data["source"],
        )
        new_item.setPolygon(QPolygonF(poly_image))

    else:
        return

    # new_item.setToolTip(create_tooltip_cropped_image(object_data['image'],
    #                                                 object_data['image_id'],
    #                                                 object_type,
    #                                                 object_data['resight_set'],
    #                                                 reviewed=object_data['reviewed'],
    #                                                 source=object_data['source']))
    scene.addItem(new_item)


def loader_image_geom(
    db: DBHandler,
    scene: ImageScene,
    image: WISDAMImage,
    point_size: int,
    color_attribute: str,
    default_dict: dict | None = None,
    default_value=None,
):
    # get color dict from db values with lookup table of attribute and DB column name
    color_attribute_db = look_up_attribute_db_column[color_attribute]

    if default_value is None:
        value_default = color_attribute_db["default"]
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
            value = single_object[color_attribute_db["db_name"]]
            if value is None:
                value = value_default
            if value not in color_values and value is not None:
                color_values.append(value)

        for single_object in data_reprojection:
            value = single_object[color_attribute_db["db_name"]]
            if value is None:
                value = value_default
            if value not in color_values and value is not None:
                color_values.append(value)

        color_values.sort()

        if default_value is not None:
            if default_value in color_values:
                color_values.insert(
                    0, color_values.pop(color_values.index(default_value))
                )
            else:
                color_values.insert(0, default_value)

        color_dict = {
            "attribute": color_attribute,
            "colors": get_new_color_dict_objects(color_values),
        }

    if data_from_image:
        for single_object in data_from_image:
            value = single_object[color_attribute_db["db_name"]]
            if value is None:
                value = value_default

            if value is not None:
                draw_geometry(
                    scene,
                    single_object,
                    point_size,
                    color_dict["colors"].get(
                        value, ColorGui.color_invalid_attribute_scenes
                    ),
                )
            else:
                draw_geometry(
                    scene,
                    single_object,
                    point_size,
                    ColorGui.color_invalid_attribute_scenes,
                )

    # load geom from other images

    if data_reprojection:
        for single_object in data_reprojection:
            value = single_object[color_attribute_db["db_name"]]
            if value is None:
                value = value_default
            if value is not None:
                draw_geometry_projections(
                    scene,
                    image,
                    single_object,
                    point_size,
                    color_dict["colors"].get(
                        value, ColorGui.color_invalid_attribute_scenes
                    ),
                )
            else:
                draw_geometry_projections(
                    scene,
                    image,
                    single_object,
                    point_size,
                    ColorGui.color_invalid_attribute_scenes,
                )

    return color_dict
