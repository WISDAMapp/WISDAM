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
import numpy as np
from numpy import sin, cos
from pathlib import Path

from pyproj import CRS
from pyproj.crs import CompoundCRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

logger = logging.getLogger(__name__)


class VARDAMurdoch(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'ScanEagle Murdoch'
        self.loader_type = LoaderType.EXIF_Loader

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        """

        return None

    def extract_logfile(self, log_file: Path) -> object | None:

        return None

    def get(self,  **kwargs) -> tuple[ImageBase, int, int] | None:

        meta_data = kwargs.pop('meta_data')

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)
        position = None
        orientation = None
        crs = None

        if width is None or height is None:
            return None

        if {'EXIF:GPSLongitude', 'EXIF:GPSLatitude', 'EXIF:GPSAltitude'} <= meta_data.keys():

            x_exif = meta_data.get('EXIF:GPSLongitude', None)
            if meta_data.get('EXIF:GPSLongitudeRef', 'E') == 'W':
                x_exif = -x_exif
            y_exif = meta_data.get('EXIF:GPSLatitude', None)
            if meta_data.get('EXIF:GPSLatitudeRef', 'S') == 'S':
                y_exif = -y_exif
            z_exif = meta_data.get('EXIF:GPSAltitude', None)

            crs_hor_exif = meta_data.get('XMP:HorizCS', 4979)
            crs_vert_exif = meta_data.get('XMP:VertCS', 'ellipsoidal')

            if crs_vert_exif == 'ellipsoidal':
                crs_exif = CRS(crs_hor_exif).to_3d()
            else:
                crs_exif = CompoundCRS(str(crs_hor_exif) + '+'+str(crs_vert_exif), [crs_hor_exif, crs_vert_exif])

            result = point_convert_utm_wgs84_egm2008(crs_exif, x_exif, y_exif, z_exif)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

        if 'EXIF:GPSMapDatum' in meta_data.keys():
            # 380527518
            rot_coded_roll = float(str(meta_data['EXIF:GPSMapDatum'])[0:3])
            rot_coded_pith = float(str(meta_data['EXIF:GPSMapDatum'])[3:6])
            rot_coded_yaw = float(str(meta_data['EXIF:GPSMapDatum'])[6:])
            pitch = (rot_coded_pith - 500.0) / 10.0 * np.pi / 180.0
            roll = (rot_coded_roll - 500.0) / 10.0 * np.pi / 180.0

            if roll > 0:
                roll = -roll
            else:
                pitch = -pitch
            yaw = (-90.0 - rot_coded_yaw / 2.0) * np.pi / 180.0

            # Rotation of IMAGE
            rot_sys = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                 cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                 cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

            rot_cam = np.array([-rot_sys[:, 1], rot_sys[:, 0], rot_sys[:, 2]]).transpose()
            orientation = Rotation(rot_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, crs=crs,
                                 position=position, orientation=orientation)

        return image, width, height
