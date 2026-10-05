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
from pyproj import CRS
from pathlib import Path

from importer.loaderImageBase import ImageBaseLoader, LoaderType

# weitsicht
from weitsicht.image.base_class import ImageBase
from weitsicht.image.perspective import ImagePerspective
from weitsicht.metadata.camera_estimator_metadata import ior_from_meta
from weitsicht.metadata.tag_systems.pyexiftool_tags import PyExifToolTags

logger = logging.getLogger(__name__)


class SimpleImage(ImageBaseLoader):
    def __init__(self):
        super().__init__()
        self.name = "Simple Perspective Image"
        self.loader_type = LoaderType.SimpleImage_Loader

    @staticmethod
    def info_text() -> str | None:

        text = (
            "This importer will import images only for annotations/verification."
            "\nNo goe-reference information will be stored.\n"
            "Image footprint and objects can not be mapped."
        )

        return text

    @staticmethod
    def logfile_suffix() -> list[str] | None:
        """return the possible suffixes of your logfiles in the format as: ['*.csv'] or ['*.txt', '*.csv']"""

        return None

    def extract_logfile(self, log_file: Path, recursive: bool = False) -> object | None:

        return None

    def get(
        self, image_path: Path, meta_data: dict, **kwargs
    ) -> tuple[ImageBase, int, int] | None:

        # georef_input: list = kwargs.pop('georef_input')
        crs_data: CRS | None = kwargs.pop("crs")

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

        # if georef_input:
        # crs = crs
        # heading = -numpy.deg2rad(georef_input[3])
        # rot_cam = numpy.array([[cos(heading), -sin(heading), 0], [sin(heading), cos(heading), 0], [0, 0, 1]])
        # image._orientation = Rotation(rot_cam)
        #    pass

        # No pose: this importer intentionally loads images without geo-reference (for annotation/verification only).
        image = ImagePerspective(
            width=ior_res.width,
            height=ior_res.height,
            camera=ior_res.camera,
            crs=crs_data,
        )

        return image, int(image.width), int(image.height)
