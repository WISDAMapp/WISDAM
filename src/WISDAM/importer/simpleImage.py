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
from pyproj import CRS
from pathlib import Path

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# WISDAM core
from WISDAMcore.image.base_class import ImageBase
from WISDAMcore.image.perspective import IMAGEPerspective
from WISDAMcore.transform.utm_converter import point_convert_utm_wgs84_egm2008
from WISDAMcore.transform.rotation import Rotation
from WISDAMcore.camera.model_selector import estimate_camera_from_meta_dict

logger = logging.getLogger(__name__)


class SimpleImage(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = 'Simple Perspective Image'
        self.loader_type = LoaderType.SimpleImage_Loader
        #self.loader_type = LoaderType.SimpleImage_Loader

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']
        """

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        return None

    def get(self, image_path: Path, meta_data: dict, **kwargs) -> tuple[ImageBase, int, int] | None:

        # georef_input: list = kwargs.pop('georef_input')
        crs_data: CRS | None = kwargs.pop('crs')

        camera, width, height = estimate_camera_from_meta_dict(meta_dict=meta_data)
        position = None
        orientation = None

        if width is None or height is None:
            return None

        # if georef_input:
            # crs = crs
            # heading = -numpy.deg2rad(georef_input[3])
            # rot_cam = numpy.array([[cos(heading), -sin(heading), 0], [sin(heading), cos(heading), 0], [0, 0, 1]])
            # image._orientation = Rotation(rot_cam)
        #    pass

        image = IMAGEPerspective(width=width, height=height, camera=camera, position=position,
                                 orientation=orientation, crs=crs_data)

        return image, width, height
