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
from collections.abc import Mapping
from functools import lru_cache

from pyproj import Transformer
from shapely import geometry
from shapely.geometry.base import BaseGeometry
from shapely.ops import transform
from weitsicht.transform.utm_converter import get_zone


WGS84_CRS = 4326


@lru_cache(maxsize=8)
def _transformer_to_crs(target_crs: int) -> Transformer:
    return Transformer.from_crs(WGS84_CRS, target_crs, always_xy=True)


def _load_geojson_geometry(geojson: str | dict) -> BaseGeometry | None:
    if not geojson:
        return None

    if isinstance(geojson, str):
        geojson = json.loads(geojson)

    if not isinstance(geojson, Mapping):
        return None

    if geojson.get("type") == "Feature":
        geojson = geojson.get("geometry")

    if not geojson:
        return None

    geom = geometry.shape(geojson)
    if geom.is_empty:
        return None

    return geom


def _get_geometry_utm_crs(geom: BaseGeometry) -> int:
    point = geom.representative_point()
    return get_zone(point.x, point.y)


def _rectangle_side_lengths(rect: BaseGeometry) -> tuple[float, float]:
    if rect.geom_type == "Point":
        return 0.0, 0.0

    if rect.geom_type == "LineString":
        return rect.length, 0.0

    if rect.geom_type != "Polygon":
        return 0.0, 0.0

    coords = list(rect.exterior.coords)
    if len(coords) < 4:
        return 0.0, 0.0

    side_lengths = [
        geometry.Point(coords[idx]).distance(geometry.Point(coords[idx + 1]))
        for idx in range(4)
    ]
    side_lengths_non_zero = [length for length in side_lengths if length > 0.0]

    return max(side_lengths), min(
        side_lengths_non_zero
    ) if side_lengths_non_zero else 0.0


def minimum_bounding_box_dimensions(
    geojson: str | dict, target_crs: int | None = None
) -> dict[str, float] | None:
    """Return oriented minimum bounding box dimensions for WGS84 GeoJSON geometry.

    Coordinates are interpreted as lon/lat WGS84. If no target CRS is given, the
    UTM EPSG code is estimated from the geometry before the minimum rotated
    rectangle is calculated. Z values are ignored.
    """

    geom = _load_geojson_geometry(geojson)
    if geom is None:
        return None

    if target_crs is None:
        target_crs = _get_geometry_utm_crs(geom)

    transformer = _transformer_to_crs(target_crs)

    def project_xy(x, y, z=None):
        return transformer.transform(x, y)

    geom_projected = transform(project_xy, geom)
    minimum_rect = geom_projected.minimum_rotated_rectangle
    length_m, width_m = _rectangle_side_lengths(minimum_rect)
    length_m = round(length_m, 3)
    width_m = round(width_m, 3)

    return {
        "bbox_length_m": length_m,
        "bbox_width_m": width_m,
        "bbox_area_m2": round(length_m * width_m, 6),
    }
