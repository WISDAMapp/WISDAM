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


from __future__ import annotations
import logging
from pathlib import Path
import json
from pyproj import CRS
from shapely import geometry
import numpy as np

from weitsicht import ArrayNx2
from weitsicht.image.image_dict_selector import get_image_from_dict
from weitsicht.image.base_class import ImageBase
from weitsicht.mapping.base_class import MappingBase
from weitsicht.transform.coordinates_transformer import CoordinateTransformer
from weitsicht.exceptions import (
    WeitsichtError,
    CoordinateTransformationError,
)
from proj_warnings import is_probable_proj_grid_error, log_proj_grid_warning_once


logger = logging.getLogger(__name__)


def _log_mapping_result_failure_once(
    key: str,
    action: str,
    result,
    image_path: Path | None,
) -> None:
    error = getattr(result, "error", None)
    if is_probable_proj_grid_error(error):
        log_proj_grid_warning_once(logger, key, action, error, image_path)


class WISDAMImage:
    def _transform_to_epsg4979(self, coordinates: np.ndarray) -> np.ndarray:
        """
        Transform coordinates from the image CRS to EPSG:4979 (WGS84 3D).

        Uses weitsicht's CoordinateTransformer to reflect the current weitsicht module.
        """
        if self.image_model is None:
            raise CoordinateTransformationError("No image model available")

        coo = np.asarray(coordinates)
        if coo.ndim == 1:
            coo = coo.reshape(1, -1)

        # weitsicht CoordinateTransformer.from_crs() returns a transformer (or None if no transform required),
        # and the actual transformation is done via transformer.transform(coordinates).
        # Pattern used in weitsicht itself: build transformer, apply if not None, else passthrough.
        transformer = CoordinateTransformer.from_crs(self.image_model.crs, CRS(4979))
        if transformer is None:
            return coo

        return np.asarray(transformer.transform(coo))

    def __init__(
        self,
        image_id: int = 0,
        importer: str = "",
        path: Path = Path(""),
        image_datetime: str = "",
        inspected: int = 0,
        width: int = 0,
        height: int = 0,
        image_model: ImageBase = None,
        gsd: float = 0.0,
        area: float = 0.0,
        meta_user: dict | None = None,
        meta_image: dict | None = None,
        group_image: int = 0,
        transect: str | None = None,
        block: str | None = None,
        flight_ref: str | None = None,
        footprint: None = None,
        center_point: None = None,
        position_wgs84: None = None,
    ):

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
        if data.get("math_model") is not None:
            param_dict = json.loads(data["math_model"])
            image_model = get_image_from_dict(param_dict=param_dict, mapper=mapper)

        importer = data["importer"]
        image_id = data["id"]
        path = Path(data["path"])

        inspected = data["inspected"]
        width = data["width"]
        height = data["height"]

        gsd = data["gsd"]
        area = data["area"]

        meta_user = None
        if data.get("meta_user") is not None:
            meta_user = json.loads(data["meta_user"])

        meta_image = None
        if data.get("meta_image") is not None:
            meta_image = json.loads(data["meta_image"])

        footprint = None
        # if data.get('footprint') is not None:
        #    footprint = json.loads(data['footprint'])

        center_point = None
        if data.get("center_point_json") is not None:
            center_point = tuple(json.loads(data["center_point_json"])["coordinates"])

        position_wgs84 = None
        # if data.get('position_wgs84') is not None:
        #    position_wgs84 = json.loads(data['position_wgs84'])

        image_datetime = data["datetime"]

        transect = data["transect"]
        block = data["block"]
        flight_ref = data["flight_ref"]
        group_image = data["group_image"]

        if data["position"]:
            position_wgs84 = tuple(json.loads(data["position_json"])["coordinates"])

        image = cls(
            image_id=image_id,
            importer=importer,
            path=path,
            image_datetime=image_datetime,
            inspected=inspected,
            width=width,
            height=height,
            image_model=image_model,
            gsd=gsd,
            area=area,
            meta_user=meta_user,
            meta_image=meta_image,
            transect=transect,
            block=block,
            flight_ref=flight_ref,
            group_image=group_image,
            footprint=footprint,
            center_point=center_point,
            position_wgs84=position_wgs84,
        )

        return image

    def map_geometry_to_epsg4979(
        self, obj_id: int, geom_type: str, points_image: ArrayNx2
    ) -> tuple[int, str, np.ndarray, float, float] | None:

        if self.image_model is None:
            return None

        try:
            result = self.image_model.map_points(np.asarray(points_image))
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "object-mapping-proj-grid",
                "Object coordinate mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        if result is None or not getattr(result, "ok", False):
            _log_mapping_result_failure_once(
                "object-mapping-proj-grid",
                "Object coordinate mapping",
                result,
                self.path,
            )
            return None

        mask = getattr(result, "mask", None)
        if mask is None:
            return None
        mask_arr = np.asarray(mask, dtype=bool)
        # We only allow mappings where all points could be mapped successfully.
        if mask_arr.size == 0 or not np.all(mask_arr):
            return None

        coo = getattr(result, "coordinates", None)
        if coo is None:
            return None
        gsd = float(getattr(result, "gsd", 0.0))
        coo_arr = np.asarray(coo)

        area = 0.0
        if geom_type == "Polygon":
            footprint_geom = geometry.Polygon(coo_arr)
            area = float(np.round(footprint_geom.area))

        try:
            coo_wgs84 = self._transform_to_epsg4979(coo_arr)
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "object-mapping-proj-grid",
                "Object coordinate mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        return obj_id, geom_type, coo_wgs84, gsd, area

    def map_footprint_to_epsg4979(self) -> tuple[np.ndarray, float, float] | None:
        if self.image_model is None:
            return None

        try:
            result = self.image_model.map_footprint()
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        if result is None or not getattr(result, "ok", False):
            _log_mapping_result_failure_once(
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                result,
                self.path,
            )
            return None

        mask = getattr(result, "mask", None)
        if mask is None:
            return None
        mask_arr = np.asarray(mask, dtype=bool)
        # We only allow mappings where all points could be mapped successfully.
        if mask_arr.size == 0 or not np.all(mask_arr):
            return None

        try:
            coordinates = getattr(result, "coordinates", None)
            if coordinates is None:
                return None
            coordinates_wgs84 = self._transform_to_epsg4979(np.asarray(coordinates))
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        return (
            coordinates_wgs84,
            float(getattr(result, "gsd", 0.0)),
            float(getattr(result, "area", 0.0)),
        )

    def map_center_to_epsg4979(self) -> tuple[np.ndarray, float] | None:
        if self.image_model is None:
            return None

        try:
            result = self.image_model.map_center_point()
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        if result is None or not getattr(result, "ok", False):
            _log_mapping_result_failure_once(
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                result,
                self.path,
            )
            return None

        mask = getattr(result, "mask", None)
        if mask is None:
            return None
        mask_arr = np.asarray(mask, dtype=bool)
        # We only allow mappings where all points could be mapped successfully.
        if mask_arr.size == 0 or not np.all(mask_arr):
            return None

        try:
            coordinates = getattr(result, "coordinates", None)
            if coordinates is None:
                return None
            coordinates_wgs84 = self._transform_to_epsg4979(np.asarray(coordinates))
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "image-mapping-proj-grid",
                "Image footprint/center mapping",
                exc,
                self.path,
            )
            return None
        except (WeitsichtError, ValueError, TypeError):
            return None

        # For a point, return a flat (3,) array to keep downstream geojson creation simple.
        if coordinates_wgs84.ndim == 2 and coordinates_wgs84.shape[0] == 1:
            coordinates_wgs84 = coordinates_wgs84[0]

        return coordinates_wgs84, float(getattr(result, "gsd", 0.0))

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
        except CoordinateTransformationError as exc:
            log_proj_grid_warning_once(
                logger,
                "image-position-proj-grid",
                "Image position transformation",
                exc,
                self.path,
            )
            return None

        return res

    @property
    def shape(self) -> tuple[int, int]:
        return self.width, self.height
