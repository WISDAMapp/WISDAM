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
from pathlib import Path

from pyproj import CRS
from pyproj.crs import CompoundCRS

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


class VARDAMurdoch(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "ScanEagle Murdoch"
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text():
        return None

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']"""

        return None

    def extract_logfile(self, log_file: Path) -> object | None:

        return None

    def get(self, **kwargs) -> tuple[ImageBase, int, int] | None:

        meta_data = kwargs.pop("meta_data")
        crs_data: CRS = kwargs["crs"]
        vertical_ref: str = kwargs["vertical_ref"]
        height_rel_raw = kwargs["height_rel"]

        try:
            height_rel = float(height_rel_raw)
        except (TypeError, ValueError):
            height_rel = 0.0

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

        # --- Position / CRS ---
        gps = tags.get_standard_gps()
        if (
            gps.gps_longitude is not None
            and gps.gps_latitude is not None
            and gps.gps_altitude is not None
        ):
            x_exif = float(gps.gps_longitude)
            if str(gps.gps_longitude_ref).upper() == "W":
                x_exif = -x_exif
            y_exif = float(gps.gps_latitude)
            if str(gps.gps_latitude_ref).upper() == "S":
                y_exif = -y_exif
            z_exif = float(gps.gps_altitude)

            rel_z_exif = None
            if vertical_ref == "relative":
                # Don't go through the tag system here because it may not preserve "missing vs 0" reliably.
                rel_z_exif = meta_data.get("XMP:RelativeAltitude", None)
                if rel_z_exif is not None:
                    z_exif = height_rel + float(rel_z_exif)

            if crs_data is None:
                if vertical_ref == "orthometric":
                    crs_hor_exif = 4326
                    crs_vert_exif = 3855

                else:
                    crs_hor_exif = meta_data.get("XMP:HorizCS", 4979)
                    crs_vert_exif = meta_data.get("XMP:VertCS", "ellipsoidal")

                if meta_data.get("XMP:HorizCS", None) is not None:
                    crs_hor_exif = meta_data["XMP:HorizCS"]
                    crs_vert_exif = meta_data.get("XMP:VertCS", "ellipsoidal")

                # This is now an override if relative height is specified:
                if rel_z_exif is not None:
                    crs_hor_exif = 4326
                    crs_vert_exif = 3855

                if crs_vert_exif == "ellipsoidal":
                    crs_data = CRS(crs_hor_exif).to_3d()
                else:
                    crs_hor = CRS.from_user_input(crs_hor_exif)
                    crs_vert = CRS.from_user_input(crs_vert_exif)
                    crs_data = CompoundCRS(
                        f"{crs_hor_exif}+{crs_vert_exif}", [crs_hor, crs_vert]
                    )

            try:
                x, y, z, crs = point_convert_utm_wgs84_egm2008(
                    crs_data, x_exif, y_exif, z_exif
                )
                position = np.array([x, y, z])
            except CoordinateTransformationError as exc:
                log_proj_grid_warning_once(
                    logger,
                    "image-import-proj-grid",
                    "Image import coordinate transformation",
                    exc,
                )
                position = None
                crs = None
            except ValueError:
                position = None
                crs = None

        # --- Orientation ---
        gps_map_datum = meta_data.get("EXIF:GPSMapDatum", None)
        if gps_map_datum is not None:
            try:
                # Expected encoding like "380527518"
                s = str(gps_map_datum).strip()
                if len(s) < 7:
                    raise ValueError("EXIF:GPSMapDatum too short")

                rot_coded_roll = float(s[0:3])
                rot_coded_pith = float(s[3:6])
                rot_coded_yaw = float(s[6:])
                pitch = (rot_coded_pith - 500.0) / 10.0 * np.pi / 180.0
                roll = (rot_coded_roll - 500.0) / 10.0 * np.pi / 180.0

                if roll > 0:
                    roll = -roll
                else:
                    pitch = -pitch
                yaw = (-90.0 - rot_coded_yaw / 2.0) * np.pi / 180.0

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

                rot_cam = np.array(
                    [-rot_sys[:, 1], rot_sys[:, 0], rot_sys[:, 2]]
                ).transpose()
                orientation = Rotation(rot_cam)
            except Exception:
                logger.warning(
                    "Failed to parse EXIF:GPSMapDatum='%s'", str(gps_map_datum)
                )

        image = ImagePerspective(
            width=width,
            height=height,
            camera=camera,
            crs=crs,
            position=position,
            orientation=orientation,
        )

        return image, width, height
