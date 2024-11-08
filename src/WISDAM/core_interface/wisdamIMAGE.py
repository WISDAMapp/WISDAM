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


from __future__ import annotations
from pathlib import Path
import json
from pyproj import CRS
from shapely import geometry
import numpy as np

from WISDAMcore import ArrayNx2
from WISDAMcore.image.type_selector import get_image_from_dict
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.mapping.base_class import MappingBase
from WISDAMcore.transform.coordinates import CoordinatesTransformer
from WISDAMcore.exceptions import MappingError, CoordinateTransformationError


class WISDAMImage:

    def __init__(self, image_id: int = 0, importer: str = '', path: Path = Path(''), image_datetime: str = '',
                 inspected: int = 0, width: int = 0, height: int = 0, image_model: ImageBase = None,
                 gsd: float = 0.0, area: float = 0.0,
                 meta_user: dict | None = None, meta_image: dict | None = None, group_image: int = 0,
                 transect: str | None = None, block: str | None = None, flight_ref: str | None = None,
                 footprint: None = None, center_point: None = None, position_wgs84: None = None):

        self.id: int = image_id

        self.importer: str | None = importer

        self.path: Path | None = path
        self.datetime: str = image_datetime

        self.inspected: int = inspected

        self.width: int = width
        self.height: int = height

        self.image_model: ImageBase | None = image_model

        self.gsd: float = gsd
        self.area: float = area

        self.meta_user: dict | None = meta_user
        self.meta_image: dict | None = meta_image

        self.footprint: None = footprint
        self.center_point: None = center_point
        self.position_wgs84: None = position_wgs84

        self.group_image = group_image
        self.transect = transect
        self.block = block
        self.flight_ref = flight_ref

    @classmethod
    def from_db(cls, data: dict, mapper: MappingBase) -> WISDAMImage:

        image_model = None
        if data.get('math_model') is not None:
            param_dict = json.loads(data['math_model'])
            image_model = get_image_from_dict(param_dict=param_dict, mapper=mapper)

        importer = data['importer']
        image_id = data['id']
        path = Path(data['path'])

        inspected = data['inspected']
        width = data['width']
        height = data['height']

        gsd = data['gsd']
        area = data['area']

        meta_user = None
        if data.get('meta_user') is not None:
            meta_user = json.loads(data['meta_user'])

        meta_image = None
        if data.get('meta_image') is not None:
            meta_image = json.loads(data['meta_image'])

        footprint = None
        # if data.get('footprint') is not None:
        #    footprint = json.loads(data['footprint'])

        center_point = None
        if data.get('center_point_json') is not None:
            center_point = tuple(json.loads(data['center_point_json'])['coordinates'])

        position_wgs84 = None
        # if data.get('position_wgs84') is not None:
        #    position_wgs84 = json.loads(data['position_wgs84'])

        image_datetime = data['datetime']

        transect = data['transect']
        block = data['block']
        flight_ref = data['flight_ref']
        group_image = data['group_image']

        if data['position']:
            position_wgs84 = tuple(json.loads(data['position_json'])['coordinates'])

        image = cls(image_id=image_id, importer=importer, path=path, image_datetime=image_datetime, inspected=inspected,
                    width=width, height=height, image_model=image_model,
                    gsd=gsd, area=area,
                    meta_user=meta_user, meta_image=meta_image,
                    transect=transect, block=block, flight_ref=flight_ref, group_image=group_image,
                    footprint=footprint, center_point=center_point, position_wgs84=position_wgs84)

        return image

    def map_geometry_to_epsg4979(self,
                                 obj_id: int,
                                 geom_type: str,
                                 points_image: ArrayNx2) \
            -> tuple[float, str, CoordinatesTransformer, float, float] | None:

        if self.image_model is None:
            return None

        try:
            result = self.image_model.map_points(points_image)
        except MappingError:
            return None

        if result is None:
            return None
        coo, gsd = result

        area = 0.0
        if geom_type == 'Polygon':
            footprint_geom = geometry.Polygon(coo)
            area = float(np.round(footprint_geom.area))

        try:
            coordinates_wgs84 = CoordinatesTransformer.from_crs(self.image_model.crs, CRS.from_epsg(4979), coo)
        except CoordinateTransformationError:
            return None

        return obj_id, geom_type, coordinates_wgs84, gsd, area

    def map_footprint_to_epsg4979(self) -> tuple[CoordinatesTransformer, float, float] | None:
        try:
            result = self.image_model.map_footprint()
        except MappingError:
            return None

        if result is None:
            return None

        coordinates, gsd, area = result

        try:
            coordinates_wgs84 = CoordinatesTransformer.from_crs(self.image_model.crs, CRS.from_epsg(4979),
                                                                coordinates)
        except CoordinateTransformationError:
            return None

        return coordinates_wgs84, gsd, area

    def map_center_to_epsg4979(self) -> tuple[CoordinatesTransformer, float] | None:

        try:
            result = self.image_model.map_center_point()
        except MappingError:
            return None

        if result is None:
            return None

        coordinates, gsd = result

        try:
            coordinates_wgs84 = CoordinatesTransformer.from_crs(self.image_model.crs, CRS.from_epsg(4979),
                                                                coordinates)
        except CoordinateTransformationError:
            return None

        return coordinates_wgs84, gsd


    @property
    def is_geo_referenced(self) -> bool:

        if self.image_model is None:
            return False

        return self.image_model.is_geo_referenced

    @property
    def position_wgs84_geojson(self) -> dict | None:

        if self.image_model is None:
            return None

        try:
            res = self.image_model.position_wgs84_geojson
        except CoordinateTransformationError:
            return None

        return res

    @property
    def shape(self) -> tuple[int, int]:
        return self.width, self.height
