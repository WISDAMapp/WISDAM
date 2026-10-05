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
from weitsicht.exceptions import CoordinateTransformationError
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags
from weitsicht.transform.utm_converter import point_convert_utm_wgs84_egm2008
from weitsicht.transform.rotation import Rotation
from proj_warnings import log_proj_grid_warning_once

body_to_cam = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
swap = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

logger = logging.getLogger(__name__)


class AircraftAeroGlobe(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Aircraft AeroGlobe"
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:

        text = (
            "Specific loader for AeroGlob data.\n\n"
            "Try to use coordinate system EPSG:4326+3855 for older logfiles."
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:

        try:
            # By "usecols" we make sure all columns needed are present and the dataframe look the same for
            # concatenation later on
            data_ascii = pandas.read_csv(
                log_file,
                comment="#",
                sep=",",
                header=0,
                usecols=["ID", "LAT", "LNG", "ALT", "YAW", "PITCH", "ROLL"],
            )
            # Rename the columns to be lower case, just in case if logfile uses lower and upper case
            data_ascii.columns = [x.lower() for x in data_ascii.columns]
        except (
            pandas.errors.DataError,
            pandas.errors.ParserError,
            pandas.errors.EmptyDataError,
            ValueError,
        ):
            # Catch all possible errors and return None
            # We will not forward errors in this stage as its more data related and thus it can anyhow not be used
            # by the importer further. User gets a message if one of his logfile does not work
            return None

        # Normalize image identifiers for fast exact lookup in get().
        data_ascii["id_stem"] = data_ascii["id"].apply(
            lambda v: Path(str(v)).stem.casefold()
        )

        # Validate numeric columns early. Invalid rows can't be used for pose anyway.
        numeric_cols = ["lat", "lng", "alt", "yaw", "pitch", "roll"]
        for col in numeric_cols:
            if col in data_ascii.columns:
                data_ascii[col] = pandas.to_numeric(data_ascii[col], errors="coerce")

        invalid_mask = (
            data_ascii[numeric_cols].isna().any(axis=1) | data_ascii["id_stem"].isna()
        )
        if bool(invalid_mask.any()):
            invalid_count = int(invalid_mask.sum())
            logger.warning(
                "Dropping %d invalid rows from logfile '%s' (missing/invalid numeric values or id).",
                invalid_count,
                str(log_file),
            )
            data_ascii = data_ascii.loc[~invalid_mask].copy()

        # If the logfile has multiple rows for the same image, keep the last one deterministically.
        dup_mask = data_ascii["id_stem"].duplicated(keep=False)
        if bool(dup_mask.any()):
            dup_count_keys = int(data_ascii.loc[dup_mask, "id_stem"].nunique())
            dup_count_rows = int(dup_mask.sum())
            logger.warning(
                "Duplicate image entries in logfile '%s' (%d duplicate rows across %d image keys). "
                "Keeping the last occurrence for each image.",
                str(log_file),
                dup_count_rows,
                dup_count_keys,
            )
            data_ascii = data_ascii.drop_duplicates(subset=["id_stem"], keep="last")

        data_ascii = data_ascii.set_index("id_stem", drop=False)

        return data_ascii

    def get(
        self,
        image_path: Path,
        meta_data: dict | None = None,
        log_data: pandas.DataFrame | None = None,
        **kwargs,
    ) -> tuple[ImageBase, int, int] | None:

        # the names of the log_data pandas dataframe is defined in extract logfiles

        crs_data: CRS = kwargs["crs"]

        # not sure anymore why I did this, probably because there was some problem with the GFX camera
        # meta_data.pop("EXIF:FocalPlaneResolutionUnit")

        if meta_data is None:
            return None

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

        # Exact match on normalized stem to avoid accidental substring matches.
        key = image_path.stem.casefold()
        row = None
        try:
            match = log_data.loc[key]
            row = match.iloc[-1] if isinstance(match, pandas.DataFrame) else match
        except KeyError:
            row = None

        if row is not None:
            if crs_data is None:
                crs_data = CRS("EPSG:4979")

            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(
                    crs_data, float(row.lng), float(row.lat), float(row.alt)
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
                crs = None
            except ValueError:
                position = None
                crs = None

            pitch = float(row.pitch) * np.pi / 180
            yaw = float(row.yaw) * np.pi / 180
            roll = float(row.roll) * np.pi / 180

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
