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


# Some info about DJI tags and values

# For older DJI models there was some inconsistency in the tags
# Also the altitude was quite strange for some old models

# https://dl.djicdn.com/downloads/p4-multispectral/20200717/P4_Multispectral_Image_Processing_Guide_EN.pdf
# https://dl.djicdn.com/downloads/DJI_Mavic_3_Enterprise/20230829/Mavic_3M_Image_Processing_Guide_EN.pdf
# https://exiftool.org/TagNames/DJI.html


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

#  Angles of aircraft are defined in X forware, y right and z down
aircraft_notation_to_front_notation = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])

#  Swap from NED to ENU coordinates
swap_ned_to_enu_coo_system = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])
swap_body_cam_gimbal = np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]])


class DJIStandard(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'DJI Different Versions'
        self.loader_type = LoaderType.EXIF_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:

        text = ("DJI importer. This importer uses the image's metadata (EXIF/XMP) to get the exterior orientation.\n"
                "Be aware that over the years the meta data seem to be slightly inconsistent to what they are referring.\n\n"
                "Most problematic is the height stated. The field 'GPSAltitude' is soley used for the images altitude.\n"
                "Some models store orthometric heights based on geoid (height above mean sea level), others store ellipsoid heights in that field."
                "\n\nIf you think the projections are wrong try to use ellipsoid height.")

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        """

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        return None

    def get(self, image_path: Path, meta_data: dict, **kwargs) -> tuple[ImageBase, int, int] | None:

        crs_data: CRS = kwargs['crs']
        vertical_ref: str = kwargs['vertical_ref']
        height_rel: str = kwargs['height_rel']

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
            if meta_data.get('EXIF:GPSLatitudeRef', 'N') == 'S':
                y_exif = -y_exif

            z_exif = meta_data.get('EXIF:GPSAltitude', None)

            rel_z_exif = None
            if vertical_ref == 'relative':
                rel_z_exif = meta_data.get('XMP:RelativeAltitude', None)
                if rel_z_exif is not None:
                    z_exif = height_rel + float(rel_z_exif)

            # if meta_data.get('XMP:RelativeAltitude', None):
            #    z_exif = meta_data['XMP:RelativeAltitude']
            #    crs_hor_exif = 4326
            #    crs_vert_exif = 3855

            if crs_data is None:

                if vertical_ref == 'orthometric':
                    crs_hor_exif = 4326
                    crs_vert_exif = 3855

                else:
                    crs_hor_exif = meta_data.get('XMP:HorizCS', 4979)
                    crs_vert_exif = meta_data.get('XMP:VertCS', 'ellipsoidal')

                if meta_data.get('XMP:HorizCS', None) is not None:
                    crs_hor_exif = meta_data['XMP:HorizCS']
                    crs_vert_exif = meta_data.get('XMP:VertCS', 'ellipsoidal')

                # This is now an override if relative height is specified:
                if rel_z_exif is not None:
                    crs_hor_exif = 4326
                    crs_vert_exif = 3855

                if crs_vert_exif == 'ellipsoidal':
                    crs_data = CRS(crs_hor_exif).to_3d()
                else:
                    crs_data = CompoundCRS(str(crs_hor_exif) + '+' + str(crs_vert_exif), [crs_hor_exif, crs_vert_exif])

            result = point_convert_utm_wgs84_egm2008(crs_data, x_exif, y_exif, z_exif)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

        roll = None
        yaw = None
        pitch = None
        angle_in_direction_of_view = False

        if {'XMP:CameraRoll', 'XMP:CameraYaw', 'XMP:CameraPitch'} <= meta_data.keys():
            angle_in_direction_of_view = True
            pitch = float(meta_data['XMP:CameraPitch']) * np.pi / 180.0
            roll = float(meta_data['XMP:CameraRoll']) * np.pi / 180.0
            yaw = float(meta_data['XMP:CameraYaw']) * np.pi / 180.0

        elif {'MakerNotes:CameraRoll', 'MakerNotes:CameraYaw', 'MakerNotes:CameraPitch'} <= meta_data.keys():
            angle_in_direction_of_view = True
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
        # elif {'XMP:FlightRollDegree', 'XMP:FlightYawDegree', 'XMP:FlightPitchDegree'} <= meta_data.keys():
        #    roll = float(meta_data['XMP:FlightRollDegree']) * np.pi / 180.0
        #    yaw = float(meta_data['XMP:FlightYawDegree']) * np.pi / 180.0
        #    pitch = float(meta_data['XMP:FlightPitchDegree']) * np.pi / 180.0

        elif {'XMP:GimbalRollDegree', 'XMP:GimbalYawDegree', 'XMP:GimbalPitchDegree'} <= meta_data.keys():
            angle_in_direction_of_view = True
            roll = float(meta_data['XMP:GimbalRollDegree']) * np.pi / 180.0
            yaw = float(meta_data['XMP:GimbalYawDegree']) * np.pi / 180.0
            pitch = (float(meta_data['XMP:GimbalPitchDegree'])) * np.pi / 180.0

        elif {'MakerNotes:GimbalRollDegree',
              'MakerNotes:GimbalYawDegree',
              'MakerNotes:GimbalPitchDegree'} <= meta_data.keys():
            angle_in_direction_of_view = True
            roll = float(meta_data['MakerNotes:GimbalRollDegree']) * np.pi / 180.0
            yaw = float(meta_data['MakerNotes:GimbalYawDegree']) * np.pi / 180.0
            pitch = (float(meta_data['MakerNotes:GimbalPitchDegree'])) * np.pi / 180.0
        if pitch is not None and roll is not None and yaw is not None:

            # Rotation of IMAGE in Body System
            rot_sys = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                 cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                 cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

            # Bring rotation into the cameras coordinate system. X left, Y top, Z backwards of viewing direction
            rot_enu_body = (swap_ned_to_enu_coo_system @ rot_sys) @ aircraft_notation_to_front_notation

            # If angle_in_direction_of_view is True we will assume the Angles refere to a system where
            # the viewing direction is specified in the angles
            # The other version is that the sensor direction is the one used.
            # So for nadir images the sensor is horizontal
            if angle_in_direction_of_view:
                rot_enu_cam = rot_enu_body @ swap_body_cam_gimbal
            else:
                rot_enu_cam = rot_enu_body @ swap_body_cam

            orientation = Rotation(rot_enu_cam)

            # rot_cam = np.matmul(np.array([[0.0, 1.0, 0.0], [1.0, 0.0, 0.0], [0.0, 0.0, -1.0]]), rot_sys)
            # rot_cam = np.array([rot_cam[:, 1], - rot_cam[:, 2], -rot_cam[:, 0]]).transpose()
            # orientation = Rotation(rot_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 crs=crs, orientation=orientation)

        return image, width, height
