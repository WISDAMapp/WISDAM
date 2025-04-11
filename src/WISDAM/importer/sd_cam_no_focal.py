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
from numpy import sin, cos
import pandas
from pathlib import Path
from pyproj import CRS

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict
from WISDAMcore.metadata.camera_estimator_metadata import compute_sensor_width_in_mm, get_sensor_from_database, \
    compute_from_sensor_width
from WISDAMcore.camera.opencv_perspective import CameraOpenCVPerspective
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

body_to_cam = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
swap = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

logger = logging.getLogger(__name__)


class SdXlsxNoFocal(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'Custom SAU XLSX no FOCAL'
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

            name = 'name' in data.columns
            lat = 'latitude' in data.columns
            lon = 'longitude' in data.columns
            if not lon:
                data.rename(columns={'longtude': 'longitude'}, inplace=True)
                lon = 'longitude' in data.columns

            alt = 'altitude' in data.columns
            roll = 'roll' in data.columns
            pitch = 'pitch' in data.columns
            yaw = 'yaw' in data.columns

            if not (name and lat and lon and alt and roll and pitch and yaw):
                return None

            return data

        except Exception as e:
            print(e)
            return None

    def get(self, image_path: Path, meta_data: dict,
            log_data: pandas.DataFrame | None = None, **kwargs) -> tuple[ImageBase, int, int] | None:

        focal_length = kwargs.pop('focal_length', 35)
        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        if width is None or height is None:
            return None

        if camera is None:
            sensor_width = compute_sensor_width_in_mm(width, meta_data)
            if sensor_width is None:
                make = meta_data.get("EXIF:Make", '')
                model = meta_data.get("EXIF:Model", '')
                sensor_size = get_sensor_from_database(make=make, model=model)
                if sensor_size is None:
                    sensor_size = (35.9, 24)

                sensor_width = sensor_size[0]

            focal_pixel = compute_from_sensor_width(focal_length, sensor_width=sensor_width,
                                                    image_width=width)

            camera = CameraOpenCVPerspective(width=width, height=height, fx=focal_pixel, fy=focal_pixel,
                                             cx=width / 2, cy=height / 2)
        position = None
        orientation = None
        crs = None

        # Find image name in log file
        row = log_data.loc[log_data['name'].str.contains(image_path.stem)]
        if not row.empty:
            row = row.iloc[0]
            crs_log = CRS("EPSG:4979")

            x = float(row.longitude)
            y = float(row.latitude)
            z = float(row.altitude)

            # Due to swap from NED to ENU
            pitch = float(row.pitch) * np.pi / 180
            yaw = float(row.yaw) * np.pi / 180
            roll = float(row.roll) * np.pi / 180

            result = point_convert_utm_wgs84_egm2008(crs_log, x, y, z)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

            # Rotation of IMAGE still in Body System
            rot_sys = np.array([[cos(pitch) * cos(yaw), sin(roll) * sin(pitch) * cos(yaw) - cos(roll) * sin(yaw),
                                 cos(roll) * sin(pitch) * cos(yaw) + sin(roll) * sin(yaw)],
                                [cos(pitch) * sin(yaw), sin(roll) * sin(pitch) * sin(yaw) + cos(roll) * cos(yaw),
                                 cos(roll) * sin(pitch) * sin(yaw) - sin(roll) * cos(yaw)],
                                [-sin(pitch), sin(roll) * cos(pitch), cos(roll) * cos(pitch)]])

            # Bring rotation into the cameras coordinate system. X left, Y top, Z backwards of viewing direction
            rot_enu_body = (swap @ rot_sys) @ body_to_cam
            rot_enu_cam = rot_enu_body @ swap_body_cam
            orientation = Rotation(rot_enu_cam)

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 crs=crs, orientation=orientation)

        return image, width, height
