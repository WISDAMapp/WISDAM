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
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation

body_to_cam = np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]])
swap = np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]])
swap_body_cam = np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]])

logger = logging.getLogger(__name__)


class AircraftAeroGlobe(ImageBaseLoader):

    def __init__(self):
        super().__init__()
        self.name = 'Aircraft AeroGlobe'
        self.loader_type = LoaderType.Logfile_Loader
        self.crs_input_show = True

    @staticmethod
    def info_text() -> str | None:

        text = ("Specific loader for AeroGlob data.\n\n"
                "Try to use coordinate system EPSG:4326+3855 for older logfiles.")

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:

        return ["*.csv"]

    def extract_logfile(self, log_file: Path) -> pandas.DataFrame | None:

        try:
            # By "usecols" we make sure all columns needed are present and the dataframe look the same for
            # concatenation later on
            data_ascii = pandas.read_csv(log_file, comment="#", sep=',', header=0, usecols=["ID", "LAT", "LNG", "ALT",
                                                                                            "YAW", "PITCH", "ROLL"])
            # Rename the columns to be lower case, just in case if logfile uses lower and upper case
            data_ascii.columns = [x.lower() for x in data_ascii.columns]
        except (pandas.errors.DataError, pandas.errors.ParserError, pandas.errors.EmptyDataError, ValueError):
            # Catch all possible errors and return None
            # We will not forward errors in this stage as its more data related and thus it can anyhow not be used
            # by the importer further. User gets a message if one of his logfile does not work
            return None

        return data_ascii

    def get(self, image_path: Path, meta_data: dict | None = None,
            log_data: pandas.DataFrame | None = None, **kwargs) -> tuple[ImageBase, int, int] | None:

        # the names of the log_data pandas dataframe is defined in extract logfiles

        crs_data: CRS = kwargs['crs']

        # not sure anymore why I did this, probably because there was some problem with the GFX camera
        # meta_data.pop("EXIF:FocalPlaneResolutionUnit")

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)

        position = None
        orientation = None
        crs = None

        if width is None or height is None:
            return None

        # Find image name in log file
        data = log_data.loc[log_data['id'].str.contains(image_path.stem)]
        if not data.empty:
            data = data.iloc[0]

            if crs_data is None:
                crs_data = CRS("EPSG:4979")

            result = point_convert_utm_wgs84_egm2008(crs_data, data.lng, data.lat, data.alt)

            if result is not None:
                x, y, z, crs = result
                position = np.array([x, y, z])

            pitch = data.pitch * np.pi / 180
            yaw = data.yaw * np.pi / 180
            roll = data.roll * np.pi / 180

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
