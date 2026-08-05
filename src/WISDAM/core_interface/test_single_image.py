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
import warnings

import pyproj.exceptions
from exiftool import ExifToolHelper
from pathlib import Path
import rasterio
from pyproj import CRS

from weitsicht.metadata.camera_estimator_metadata import estimate_camera
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags


logger_rasterio = logging.getLogger("rasterio")
logger_rasterio.setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


def meta_of_image(
    image_path: Path, path_to_exiftool: Path | None = None
) -> tuple | None:

    try:
        et = ExifToolHelper(executable=path_to_exiftool.as_posix())
    except (RuntimeError, TypeError, NameError):
        logger.error("Exif tool fails")
        return None

    meta_data = et.get_tags(Path(image_path), tags=None)[0]

    tag_system = PyExifToolTags(meta_data)

    try:
        res = estimate_camera(tag_system.get_ior_base())
    except ValueError:
        logger.warning("Meta data missing or erroneous")
        et.terminate()
        return None

    et.terminate()
    width, height, focal_pixel, c_x, c_y = res

    focal_flag = True if (focal_pixel is not None and focal_pixel > 0) else False

    gps = tag_system.get_standard_gps()
    gnss = (
        gps.gps_longitude is not None
        and gps.gps_latitude is not None
        and gps.gps_altitude is not None
    )

    crs_tags = tag_system.get_crs()
    crs_hor_exif = crs_tags.horiz_cs if crs_tags.horiz_cs is not None else False
    crs_vert_exif = crs_tags.vert_cs if crs_tags.vert_cs is not None else False

    ori = tag_system.get_orientation_values()
    pose = any(
        v is not None
        for v in (
            ori.xmp_pitch,
            ori.xmp_roll,
            ori.xmp_yaw,
            ori.xmp_camera_pitch,
            ori.xmp_camera_roll,
            ori.xmp_camera_yaw,
            ori.xmp_gimbal_roll_deg,
            ori.xmp_gimbal_yaw_deg,
            ori.xmp_gimbal_pitch_deg,
            ori.maker_notes_pitch,
            ori.maker_notes_roll,
            ori.maker_notes_yaw,
            ori.maker_notes_camera_pitch,
            ori.maker_notes_camera_roll,
            ori.maker_notes_camera_yaw,
            ori.maker_notes_gimbal_roll_deg,
            ori.maker_notes_gimbal_yaw_deg,
            ori.maker_notes_gimbal_pitch_deg,
        )
    )

    return focal_flag, gnss, crs_hor_exif, crs_vert_exif, pose


def meta_of_ortho_image(image_path: Path) -> tuple | None:

    warnings.filterwarnings("ignore", category=rasterio.errors.NotGeoreferencedWarning)

    try:
        dataset = rasterio.open(image_path)

        rasterio_flag = True
        # rasterio returns identity if file has no geo-reference
        gt = False
        if not dataset.transform.is_identity:
            gt = True

        try:
            CRS(dataset.crs).to_3d()
            crs_flag = True
        except pyproj.exceptions.CRSError:
            crs_flag = False

        return rasterio_flag, gt, crs_flag

    except rasterio.RasterioIOError:
        return None
