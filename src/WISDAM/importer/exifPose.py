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

# We follow the specifications from here, but there is nothing standardized at all
# https://support.pix4d.com/hc/en-us/articles/360016450032

import logging
import numpy as np
from numpy import sin, cos
from pathlib import Path
from pyproj import CRS
from pyproj.crs import CompoundCRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

logger = logging.getLogger(__name__)

aircraft_notation_to_front_notation = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
swap_ned_to_enu_coo_system = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])


class EXIFPose(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'EXIF Pose'
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = True

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        """

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        return None

    def get(self,  image_path: Path, meta_data: dict, **kwargs) -> tuple[ImageBase, int, int] | None:

        crs_data: CRS = kwargs['crs']
        position = None
        orientation = None
        crs = None

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        if width is None or height is None:
            return None

        if {'EXIF:GPSLongitude', 'EXIF:GPSLatitude', 'EXIF:GPSAltitude'} <= meta_data.keys():

            x_exif = meta_data.get('EXIF:GPSLongitude', None)
            if meta_data.get('EXIF:GPSLongitudeRef', 'E') == 'W':
                x_exif = -x_exif
            y_exif = meta_data.get('EXIF:GPSLatitude', None)
            if meta_data.get('EXIF:GPSLatitudeRef', 'N') == 'S':
                y_exif = -y_exif
            z_exif = meta_data.get('EXIF:GPSAltitude', None)

            if crs_data is None:
                crs_hor_exif = meta_data.get('XMP:HorizCS', 4979)
                crs_vert_exif = meta_data.get('XMP:VertCS', 'ellipsoidal')

                if crs_vert_exif == 'ellipsoidal':
                    crs_data = CRS(crs_hor_exif).to_3d()
                else:
                    crs_data = CompoundCRS(str(crs_hor_exif) + '+' + str(crs_vert_exif), [crs_hor_exif, crs_vert_exif])

            result = point_convert_utm_wgs84_egm2008(crs_data, x_exif, y_exif, z_exif)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

        # Orientation
        pitch = None
        roll = None
        yaw = None
        
        if {'XMP:CameraRoll', 'XMP:CameraYaw', 'XMP:CameraPitch'} <= meta_data.keys():
            pitch = float(meta_data['XMP:CameraPitch']) * np.pi / 180.0
            roll = float(meta_data['XMP:CameraRoll']) * np.pi / 180.0
            yaw = float(meta_data['XMP:CameraYaw']) * np.pi / 180.0

        elif {'MakerNotes:CameraRoll', 'MakerNotes:CameraYaw', 'MakerNotes:CameraPitch'} <= meta_data.keys():
            pitch = float(meta_data['MakerNotes:CameraPitch']) * np.pi / 180.0
            roll = float(meta_data['MakerNotes:CameraRoll']) * np.pi / 180.0
            yaw = float(meta_data['MakerNotes:CameraYaw']) * np.pi / 180.0
        
        elif {'XMP:Roll', 'XMP:Yaw', 'XMP:Pitch'} <= meta_data.keys():
            pitch = float(meta_data.get('XMP:Pitch', 0.0)) * np.pi / 180.0
            roll = float(meta_data.get('XMP:Roll', 0.0)) * np.pi / 180.0
            yaw = float(meta_data.get('XMP:Yaw', 0.0)) * np.pi / 180.0

        elif {'MakerNotes:Roll', 'MakerNotes:Yaw', 'MakerNotes:Pitch'} <= meta_data.keys():
            pitch = float(meta_data.get('MakerNotes:Pitch', 0.0)) * np.pi / 180.0
            roll = float(meta_data.get('MakerNotes:Roll', 0.0)) * np.pi / 180.0
            yaw = float(meta_data.get('MakerNotes:Yaw', 0.0)) * np.pi / 180.0

        if pitch is not None:

            # Rotation of IMAGE still in Body System
            rot_sys = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                 cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                 cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

            # Bring rotation into the cameras coordinate system. X left, Y top, Z backwards of viewing direction
            rot_enu_body = (swap_ned_to_enu_coo_system @ rot_sys) @ aircraft_notation_to_front_notation
            rot_enu_cam = rot_enu_body @ swap_body_cam
            orientation = Rotation(rot_enu_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, crs=crs,
                                 position=position, orientation=orientation)

        return image, width, height
