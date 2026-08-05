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


import logging
import numpy as np
from numpy import sin, cos
import pandas
from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.camera.opencv_perspective import CameraOpenCVPerspective
from weitsicht.exceptions import CoordinateTransformationError
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import (
    compute_from_sensor_width,
    compute_sensor_width_in_mm,
    get_sensor_from_database,
    ior_from_meta,
)
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from weitsicht.transform.rotation import Rotation
from weitsicht.transform.utm_converter import point_convert_utm_wgs84_egm2008
from proj_warnings import log_proj_grid_warning_once

body_to_cam = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
swap = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

logger = logging.getLogger(__name__)


class SdXlsxNoFocal(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Custom SAU XLSX no FOCAL"
        self.loader_type = LoaderType.Logfile_Loader

    @staticmethod
    def info_text() -> str | None:

        return None

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.xlsx"]

    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:

        try:
            data = pandas.read_excel(log_file)

            # format columns to be lower case
            data.columns = [x.lower() for x in data.columns]

            name = "name" in data.columns
            lat = "latitude" in data.columns
            lon = "longitude" in data.columns
            if not lon:
                data.rename(columns={"longtude": "longitude"}, inplace=True)
                lon = "longitude" in data.columns

            alt = "altitude" in data.columns
            roll = "roll" in data.columns
            pitch = "pitch" in data.columns
            yaw = "yaw" in data.columns

            if not (name and lat and lon and alt and roll and pitch and yaw):
                return None

            # Validate numeric columns early. Invalid rows can't be used for pose anyway.
            numeric_cols = ["latitude", "longitude", "altitude", "roll", "pitch", "yaw"]
            for col in numeric_cols:
                data[col] = pandas.to_numeric(data[col], errors="coerce")

            # Normalize the key used for matching images and index by it for fast exact lookups.
            data["name_stem"] = data["name"].apply(
                lambda v: Path(str(v)).stem.casefold()
            )

            invalid_mask = (
                data[numeric_cols].isna().any(axis=1) | data["name_stem"].isna()
            )
            if bool(invalid_mask.any()):
                invalid_count = int(invalid_mask.sum())
                logger.warning(
                    "Dropping %d invalid rows from logfile '%s' (missing/invalid numeric values or name).",
                    invalid_count,
                    str(log_file),
                )
                data = data.loc[~invalid_mask].copy()

            # If the logfile has multiple rows for the same image, keep the last one deterministically.
            dup_mask = data["name_stem"].duplicated(keep=False)
            if bool(dup_mask.any()):
                dup_count_keys = int(data.loc[dup_mask, "name_stem"].nunique())
                dup_count_rows = int(dup_mask.sum())
                logger.warning(
                    "Duplicate image entries in logfile '%s' (%d duplicate rows across %d image keys). "
                    "Keeping the last occurrence for each image.",
                    str(log_file),
                    dup_count_rows,
                    dup_count_keys,
                )
                data = data.drop_duplicates(subset=["name_stem"], keep="last")

            data = data.set_index("name_stem", drop=False)

            return data

        except Exception:
            logger.exception("Failed to read logfile '%s'", str(log_file))
            return None

    def get(
        self,
        image_path: Path,
        meta_data: dict,
        log_data: pandas.DataFrame | None = None,
        **kwargs,
    ) -> tuple[ImageBase, int, int] | None:

        focal_length = float(kwargs.pop("focal_length", 35))

        tags = PyExifToolTags(meta_data)
        ior_res = ior_from_meta(
            tags_ior=tags.get_ior_base(), tags_ior_extended=tags.get_ior_extended()
        )
        if ior_res.ok:
            camera, width, height = ior_res.camera, ior_res.width, ior_res.height
        else:
            logger.warning(
                "weitsicht ior_from_meta failed: %s",
                getattr(ior_res, "error", "unknown error"),
            )
            # No focal length in metadata: build a minimal camera from sensor size and user-provided focal length.
            width, height = tags.get_ior_base().image_shape
            if width == 0 or height == 0:
                return None
            camera = None

        if camera is None:
            sensor_width = compute_sensor_width_in_mm(width, tags.get_ior_base())
            if sensor_width is None:
                base_tags = tags.get_ior_base()
                sensor_size = get_sensor_from_database(
                    make=base_tags.make, model=base_tags.model
                )
                if sensor_size is None:
                    sensor_size = (35.9, 24)

                sensor_width = sensor_size[0]

            focal_pixel = compute_from_sensor_width(
                focal_length, sensor_width=sensor_width, image_width=width
            )

            camera = CameraOpenCVPerspective(
                width=width,
                height=height,
                fx=focal_pixel,
                fy=focal_pixel,
                cx=width / 2,
                cy=height / 2,
            )
        position = None
        orientation = None
        crs = None

        if log_data is None:
            return None

        # Exact match on normalized stem to avoid accidental substring matches.
        row = None
        try:
            match = log_data.loc[image_path.stem.casefold()]
            row = match.iloc[-1] if isinstance(match, pandas.DataFrame) else match
        except KeyError:
            row = None

        if row is not None:
            crs_log = CRS("EPSG:4979")

            x = float(row.longitude)
            y = float(row.latitude)
            z = float(row.altitude)

            # Due to swap from NED to ENU
            pitch = float(row.pitch) * np.pi / 180
            yaw = float(row.yaw) * np.pi / 180
            roll = float(row.roll) * np.pi / 180

            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(crs_log, x, y, z)
                position = np.array([x, y, z])
            except CoordinateTransformationError as exc:
                log_proj_grid_warning_once(
                    logger,
                    "image-import-proj-grid",
                    "Image import coordinate transformation",
                    exc,
                    image_path,
                )
                position = None
                crs = None
            except ValueError:
                position = None
                crs = None

            # Rotation of IMAGE still in Body System
            rot_sys = np.array(
                [
                    [
                        cos(pitch) * cos(yaw),
                        sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                        cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw),
                    ],
                    [
                        cos(pitch) * sin(yaw),
                        sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                        cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw),
                    ],
                    [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)],
                ]
            )

            # Bring rotation into the cameras coordinate system. X left, Y top, Z backwards of viewing direction
            rot_enu_body = (swap @ rot_sys) @ body_to_cam
            rot_enu_cam = rot_enu_body @ swap_body_cam
            orientation = Rotation(rot_enu_cam)

        image = ImagePerspective(
            width=width,
            height=height,
            camera=camera,
            position=position,
            crs=crs,
            orientation=orientation,
        )

        return image, width, height
