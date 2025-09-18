# ==============================================================================
# This file is part of the WISDAM distribution
# https://github.com/WISDAMapp/WISDAM
# Copyright (C) 2025 Martin Wieser.
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

# WISDAM core
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

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
        self.name = 'Custom UTAS v1'
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True
        self.crs_input_mandatory = True
        self.log_file_contains_image_path = False

    @staticmethod
    def info_text() -> str | None:

        text = ("Importer using CSV file and img_name,x,y,z,yaw,pitch,roll angles"
                "\n\nSeperator for columns is ','. There should be no header\n"
                "Yaw, Pitch, Roll corresponds to forward looking aircraft notation North East Down\n"
                "The camera is mounted so that its looking down with the long image side crosswise to the flight strip"
                "Yaw, Pitch, Roll angles are in degree.\nThe image name has to match the real one (including suffix)\n"
                "The Coordinate system is mandatory to specify")

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv", "*.txt"]

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        # Load Logfile
        try:
            data_pandas = pandas.read_csv(log_file, sep=',', header=None)
        except (pandas.errors.DataError, pandas.errors.ParserError):
            return None

        return data_pandas

    def get(self, image_path: Path, meta_data: dict,
            log_data: pandas.DataFrame | None = None, **kwargs) -> tuple[ImageBase, int, int] | None:

        crs_data: CRS = kwargs['crs']

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        position = None
        orientation = None
        crs = None

        if width is None or height is None:
            return None

        # Find image name in log file

        # Find image name in log file
        row = log_data.loc[log_data[0].str.contains(image_path.stem)]
        if not row.empty:
            row = row.iloc[0]

            x_exif = meta_data.get('EXIF:GPSLongitude', None)
            y_exif = meta_data.get('EXIF:GPSLatitude', None)
            if meta_data.get('EXIF:GPSLongitudeRef', 'E') == 'W':
                x_exif = -x_exif
            if meta_data.get('EXIF:GPSLatitudeRef', 'N') == 'S':
                y_exif = -y_exif

            crs = crs_data.to_3d()
            #crs_exif = CRS("EPSG:4326+3855")
            result = point_convert_utm_wgs84_egm2008(crs, row[1], row[2], row[3])

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

            p = Proj(crs)
            meridian_convergence = 0
            if (x_exif is not None) and (y_exif is not None):
                facts = p.get_factors(x_exif, y_exif)
                meridian_convergence = facts.meridian_convergence

            roll = row[6] * np.pi / 180
            yaw = (row[4]-meridian_convergence) * np.pi / 180
            pitch = row[5] * np.pi / 180

            # Rotation of IMAGE
            rot_sys = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                 cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                 cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

            # Bring rotation into the cameras coordinate system. X left, Y top, Z backwards of viewing direction
            rot_enu_body = (swap_ned_to_enu_coo_system @ rot_sys) @ aircraft_notation_to_front_notation
            rat_cam = rot_enu_body @ swap_body_cam
            orientation = Rotation(rat_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 crs=crs, orientation=orientation)

        return image, width, height
