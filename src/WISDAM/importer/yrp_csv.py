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
import pandas
from pathlib import Path
from pyproj import CRS, Proj
from numpy import sin, cos

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.exceptions import CoordinateTransformationError
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from weitsicht.transform.utm_converter import point_convert_utm_wgs84_egm2008
from weitsicht.transform.rotation import Rotation
from proj_warnings import log_proj_grid_warning_once

logger = logging.getLogger(__name__)


#  Angles of aircraft are defined in X forware, y right and z down
aircraft_notation_to_front_notation = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])

#  Swap from NED to ENU coordinates
swap_ned_to_enu_coo_system = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
swap_body_cam_gimbal = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]])


class YawPitchRollCSV(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Custom UTAS v1"
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True
        self.crs_input_mandatory = True
        self.log_file_contains_image_path = False

    @staticmethod
    def info_text() -> str | None:

        text = (
            "Importer using CSV file and img_name,x,y,z,yaw,pitch,roll angles"
            "\n\nSeperator for columns is ','. There should be no header\n"
            "Yaw, Pitch, Roll corresponds to forward looking aircraft notation North East Down\n"
            "The camera is mounted so that its looking down with the long image side crosswise to the flight strip"
            "Yaw, Pitch, Roll angles are in degree.\nThe image name has to match the real one (including suffix)\n"
            "The Coordinate system is mandatory to specify"
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv", "*.txt"]

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        # Load Logfile
        try:
            data_pandas = pandas.read_csv(log_file, sep=",", header=None)
        except (pandas.errors.DataError, pandas.errors.ParserError):
            return None

        # Expect 7 columns: img_name,x,y,z,yaw,pitch,roll (no header)
        if data_pandas.shape[1] < 7:
            return None

        data_pandas = data_pandas.iloc[:, :7].copy()
        data_pandas = data_pandas.rename(
            columns={
                0: "name",
                1: "x",
                2: "y",
                3: "z",
                4: "yaw",
                5: "pitch",
                6: "roll",
            }
        )

        # Normalize image identifiers for fast exact lookup in get().
        # The logfile expects "including suffix", so match by filename (not stem) and case-insensitively.
        data_pandas["name_key"] = data_pandas["name"].apply(
            lambda v: Path(str(v)).name.casefold()
        )

        # Validate numeric columns early. Invalid rows can't be used for pose anyway.
        numeric_cols = ["x", "y", "z", "yaw", "pitch", "roll"]
        for col in numeric_cols:
            data_pandas[col] = pandas.to_numeric(data_pandas[col], errors="coerce")

        invalid_mask = (
            data_pandas[numeric_cols].isna().any(axis=1)
            | data_pandas["name_key"].isna()
        )
        if bool(invalid_mask.any()):
            invalid_count = int(invalid_mask.sum())
            logger.warning(
                "Dropping %d invalid rows from logfile '%s' (missing/invalid numeric values or name).",
                invalid_count,
                str(log_file),
            )
            data_pandas = data_pandas.loc[~invalid_mask].copy()

        # If the logfile has multiple rows for the same image, keep the last one deterministically.
        dup_mask = data_pandas["name_key"].duplicated(keep=False)
        if bool(dup_mask.any()):
            dup_count_keys = int(data_pandas.loc[dup_mask, "name_key"].nunique())
            dup_count_rows = int(dup_mask.sum())
            logger.warning(
                "Duplicate image entries in logfile '%s' (%d duplicate rows across %d image keys). "
                "Keeping the last occurrence for each image.",
                str(log_file),
                dup_count_rows,
                dup_count_keys,
            )
            data_pandas = data_pandas.drop_duplicates(subset=["name_key"], keep="last")

        data_pandas = data_pandas.set_index("name_key", drop=False)

        return data_pandas

    def get(
        self,
        image_path: Path,
        meta_data: dict,
        log_data: pandas.DataFrame | None = None,
        **kwargs,
    ) -> tuple[ImageBase, int, int] | None:

        crs_data: CRS = kwargs["crs"]

        tags = PyExifToolTags(meta_data)
        ior_res = ior_from_meta(
            tags_ior=tags.get_ior_base(), tags_ior_extended=tags.get_ior_extended()
        )
        if ior_res.ok is False:
            logger.warning(
                "weitsicht ior_from_meta failed: %s",
                getattr(ior_res, "error", "unknown error"),
            )
            return None

        camera, width, height = ior_res.camera, ior_res.width, ior_res.height

        position = None
        orientation = None
        crs = None

        if log_data is None:
            return None

        # Exact match on normalized filename (case-insensitive).
        key = image_path.name.casefold()
        row = None
        try:
            match = log_data.loc[key]
            row = match.iloc[-1] if isinstance(match, pandas.DataFrame) else match
        except KeyError:
            row = None

        if row is not None:
            x_exif = meta_data.get("EXIF:GPSLongitude", None)
            y_exif = meta_data.get("EXIF:GPSLatitude", None)
            if meta_data.get("EXIF:GPSLongitudeRef", "E") == "W":
                x_exif = -x_exif
            if meta_data.get("EXIF:GPSLatitudeRef", "N") == "S":
                y_exif = -y_exif

            crs_3d = crs_data.to_3d()
            crs = crs_3d
            # crs_exif = CRS("EPSG:4326+3855")
            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(
                    crs_3d, float(row.x), float(row.y), float(row.z)
                )
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
                crs = crs_3d
            except ValueError:
                position = None
                crs = crs_3d

            p = Proj(crs)
            meridian_convergence = 0
            if (x_exif is not None) and (y_exif is not None):
                facts = p.get_factors(x_exif, y_exif)
                meridian_convergence = facts.meridian_convergence

            roll = float(row.roll) * np.pi / 180
            yaw = (float(row.yaw) - meridian_convergence) * np.pi / 180
            pitch = float(row.pitch) * np.pi / 180

            # Rotation of IMAGE
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
            rot_enu_body = (
                swap_ned_to_enu_coo_system @ rot_sys
            ) @ aircraft_notation_to_front_notation
            rat_cam = rot_enu_body @ swap_body_cam
            orientation = Rotation(rat_cam)

        image = ImagePerspective(
            width=width,
            height=height,
            camera=camera,
            position=position,
            crs=crs,
            orientation=orientation,
        )

        return image, width, height
