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
import warnings

import pyproj.exceptions
from exiftool import ExifToolHelper
from pathlib import Path
import imghdr
import rasterio
from pyproj import CRS

from WISDAMcore.metadata.camera_estimator_metadata import estimate_camera


logger_rasterio = logging.getLogger("rasterio")
logger_rasterio.setLevel(logging.CRITICAL)

logger = logging.getLogger(__name__)


def meta_of_image(image_path: Path, path_to_exiftool: Path | None = None) -> tuple | None:
    if imghdr.what(image_path):

        try:
            et = ExifToolHelper(executable=path_to_exiftool.as_posix())
        except (RuntimeError, TypeError, NameError):
            logger.error('Exif tool fails')
            return None

        meta_data = et.get_tags(Path(image_path), tags=None)[0]
        res = estimate_camera(meta_data)
        et.terminate()

        if res is None:
            logger.warning("Meta data missing or erroneous")
            return None

        width, height, focal_pixel, c_x, c_y = res

        focal_flag = True if (focal_pixel is not None and focal_pixel > 0) else False

        gnss = True if 'EXIF:GPSLongitude' and 'EXIF:GPSLatitude' and 'EXIF:GPSAltitude' in meta_data.keys() else False
        crs_hor_exif = meta_data.get('XMP:HorizCS', False)
        crs_vert_exif = meta_data.get('XMP:VertCS', False)

        pose = True if 'XMP:Roll' and 'XMP:Yaw' and 'XMP:Pitch' in meta_data.keys() else False
        pose_dji = True if 'XMP:CameraRoll' and 'XMP:CameraYaw' and 'XMP:CameraPitch' in meta_data.keys() else False
        pose_dji_gimbal = True if 'XMP:GimbalRollDegree' and 'XMP:GimbalYawDegree' and \
                                  'XMP:GimbalPitchDegree' in meta_data.keys() else False
        return focal_flag, gnss, crs_hor_exif, crs_vert_exif, pose | pose_dji | pose_dji_gimbal

    return None


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
